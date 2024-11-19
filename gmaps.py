import requests
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

def get_bairro_e_logradouro(latitude, longitude):
    """
    Função para obter o bairro e logradouro a partir das coordenadas de latitude e longitude usando a API do Google Maps.
    """
    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={latitude},{longitude}&key={GOOGLE_MAPS_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'OK':
            bairro = None
            logradouro = None
            for result in data['results']:
                for component in result['address_components']:
                    if 'sublocality_level_1' in component['types']:
                        bairro = component['long_name']
                    if 'route' in component['types']:
                        logradouro = component['long_name']
            return bairro, logradouro
        else:
            return "Erro na Geocodificação", None
    else:
        return f"Erro: {response.status_code}", None

st.title("Consulta de Bairro e Logradouro")
st.write("Insira as coordenadas de latitude e longitude para obter o bairro e logradouro correspondentes.")

latitude = st.text_input("Latitude")
longitude = st.text_input("Longitude")

if st.button("Consultar"):
    if latitude and longitude:
        try:
            latitude = float(latitude)
            longitude = float(longitude)
            bairro, logradouro = get_bairro_e_logradouro(latitude, longitude)
            st.write(f"Bairro: {bairro}")
            st.write(f"Logradouro: {logradouro}")
        except ValueError:
            st.write("Por favor, insira valores válidos para latitude e longitude.")
    else:
        st.write("Por favor, insira ambos os valores de latitude e longitude.")