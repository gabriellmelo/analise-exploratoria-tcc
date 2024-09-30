import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import maritalk
import os
from dotenv import load_dotenv
from PIL import Image
Image.MAX_IMAGE_PIXELS = None  # Isso desativa a proteção contra "Decompression Bomb"

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Carregar a chave da API Maritaca
MARIACA_API_KEY = os.getenv("MARITACA_API_KEY")

# Função para detectar o tipo de pergunta
def detectar_tipo_pergunta(pergunta):
    if "ano" in pergunta.lower():
        return "ano"
    elif "faixa etária" in pergunta.lower():
        return "faixa_etaria"
    elif "dia da semana" in pergunta.lower():
        return "dia_semana"
    else:
        return "geral"

# Função para gerar o contexto apropriado com base nos dados
def gerar_contexto(data, tipo_pergunta):
    if tipo_pergunta == "ano":
        obitos_por_ano = data.groupby('Ano do BO')['Ano do BO'].count().to_dict()
        contexto = "Aqui estão os óbitos em Franca por ano:\n"
        for ano, qtd in obitos_por_ano.items():
            contexto += f"No ano de {ano}, houve {qtd} óbitos.\n"
    elif tipo_pergunta == "faixa_etaria":
        obitos_por_faixa = data.groupby('Faixa etaria')['Faixa etaria'].count().to_dict()
        contexto = "Aqui estão os óbitos por faixa etária:\n"
        for faixa, qtd in obitos_por_faixa.items():
            contexto += f"Na faixa etária {faixa}, houve {qtd} óbitos.\n"
    elif tipo_pergunta == "dia_semana":
        obitos_por_dia = data.groupby('Dia da Semana')['Dia da Semana'].count().to_dict()
        contexto = "Aqui estão os óbitos por dia da semana:\n"
        for dia, qtd in obitos_por_dia.items():
            contexto += f"No dia {dia}, houve {qtd} óbitos.\n"
    else:
        contexto = "Aqui estão os dados gerais sobre os óbitos em Franca."
    
    return contexto

# Função para obter resposta da Mariaca AI com o contexto gerado
def obter_resposta_maritaca_ai(pergunta, data):
    try:
        # Detectar o tipo de pergunta
        tipo_pergunta = detectar_tipo_pergunta(pergunta)
        
        # Gerar o contexto com base no tipo de pergunta
        contexto = gerar_contexto(data, tipo_pergunta)
        
        # Combinar a pergunta com o contexto
        pergunta_com_contexto = f"{contexto}\n\nPergunta: {pergunta}"
        
        # Configurar o modelo Maritaca AI
        model = maritalk.MariTalk(
            key=MARIACA_API_KEY,
            model="sabia-3"
        )
        
        # Fazer a pergunta ao modelo, limitando a 200 tokens
        response = model.generate(pergunta_com_contexto, max_tokens=200)
        answer = response["answer"]
        
        return answer
    except Exception as e:
        return f"Erro ao conectar com a API: {e}"

# Configuração da página
st.set_page_config(page_title='Análise de Óbitos em Franca/SP', layout='wide', page_icon=':bar_chart:')

col1, col2 = st.columns([0.2, 0.8])  
with col1:
    st.image('images/escudo.png', width=100)  
with col2:
    st.title("Análise de Óbitos em Acidentes de Trânsito na Cidade de Franca/SP")
    st.markdown("Fonte dos Dados Brutos: [Infosiga SP](https://www.infosiga.sp.gov.br/?name=identificacao4&contextId=8a80809939587c0901395881fc2b0004)")
    st.markdown("Código Fonte: [GitHub](https://github.com.br)")
    st.markdown("Data de Atualização: 30/09/2024")
    st.markdown("---")

# Seção de Objetivo
st.markdown("""
<div style='padding: 15px; border-radius: 10px;'>
    <p style='font-size: 16px;'>
        Esta aplicação tem como objetivo <b>analisar os dados de óbitos</b> decorrentes de acidentes de trânsito na cidade de Franca nos últimos 5 anos, 
        utilizando técnicas de análise de dados para:
    </p>
    <ul style='font-size: 16px; line-height: 1.6;'>
        <li>Identificar padrões e tendências que possam apoiar a formulação de <b>medidas preventivas</b>;</li>
        <li>Contribuir para a <b>melhoria da segurança viária</b>;</li>
        <li>Democratizar o acesso a informações, facilitando o entendimento por <b>cidadãos</b> e <b>autoridades locais</b>.</li>
    </ul>
    <p style='font-size: 16px;'>
        O projeto está alinhado com os <a href='https://brasil.un.org/pt-br/sdgs' target='_blank'>Objetivos de Desenvolvimento Sustentável (ODS)</a> da ONU, 
        em especial o <a href='https://www.ipea.gov.br/ods/ods11.html' target='_blank'>Objetivo 11</a> - Cidades e Comunidades Sustentáveis.
    </p>
</div>
""", unsafe_allow_html=True)

def load_data():
    data = pd.read_excel('filtro-franca.xlsx', sheet_name='obitos_franca')
    return data

data = load_data()

# Carregar os dados e filtrar entre os anos de 2019 a 2023
data = data[data['Ano do BO'].isin([2019, 2020, 2021, 2022, 2023])]

# Sidebar para filtro de ano
st.sidebar.header("Filtrar por Ano")
anos_disponiveis = [2019, 2020, 2021, 2022, 2023]
ano_selecionado = st.sidebar.selectbox("Escolha o Ano", ["Todos"] + [str(ano) for ano in anos_disponiveis], index=0)

# Filtrar os dados de acordo com o ano selecionado
if ano_selecionado != "Todos":
    ano_selecionado = int(ano_selecionado)
    data_filtrada = data.loc[data['Ano do BO'] == ano_selecionado]
else:
    data_filtrada = data

# Definir o ano anterior para cálculo dos deltas
if ano_selecionado != "Todos" and ano_selecionado > 2019:
    ano_anterior = ano_selecionado - 1
    dados_ano_anterior = data[data['Ano do BO'] == ano_anterior]
else:
    ano_anterior = None
    dados_ano_anterior = pd.DataFrame()

# Métricas no topo
st.subheader("Principais Insights")
col1, col2, col3 = st.columns(3)

# Total de óbitos
total_obitos = len(data_filtrada)

if ano_anterior is not None and not dados_ano_anterior.empty:
    total_obitos_anterior = len(dados_ano_anterior)
    delta_obitos = total_obitos - total_obitos_anterior
    col1.metric("Total de Óbitos", total_obitos, delta=f"{delta_obitos} comparado ao ano anterior")
else:
    with col1:
        st.metric("Total de Óbitos", total_obitos)
        st.markdown("<div style='color:orange; font-size: 14px; margin-top: -15px;'>Sem comparação</div>", unsafe_allow_html=True)

# Óbitos por Veículos Motorizados
veiculos_motorizados = data_filtrada[data_filtrada['Meio de locomocao da vitima'].isin(['MOTOCICLETA', 'AUTOMOVEL', 'CAMINHAO'])]
total_veiculos_motorizados = len(veiculos_motorizados)  # Total de veículos motorizados

if ano_anterior is not None and not dados_ano_anterior.empty:
    veiculos_motorizados_anterior = dados_ano_anterior[dados_ano_anterior['Meio de locomocao da vitima'].isin(['MOTOCICLETA', 'AUTOMOVEL', 'CAMINHAO'])]
    delta_veiculos_motorizados = total_veiculos_motorizados - len(veiculos_motorizados_anterior)
    col2.metric("Óbitos por Veículos Motorizados", total_veiculos_motorizados, delta=f"{delta_veiculos_motorizados} comparado ao ano anterior")
else:
    with col2:
        st.metric("Óbitos por Veículos Motorizados", total_veiculos_motorizados)  # Passar total de veículos motorizados
        st.markdown("<div style='color:orange; font-size: 14px; margin-top: -15px;'>Sem comparação</div>", unsafe_allow_html=True)

# Óbitos de pedestres
pedestres = data_filtrada[data_filtrada['Meio de locomocao da vitima'] == 'PEDESTRE']
total_pedestres = len(pedestres)  # Total de pedestres

if ano_anterior is not None and not dados_ano_anterior.empty:
    pedestres_anterior = dados_ano_anterior[dados_ano_anterior['Meio de locomocao da vitima'] == 'PEDESTRE']
    delta_pedestres = total_pedestres - len(pedestres_anterior)
    col3.metric("Óbitos de Pedestres", total_pedestres, delta=f"{delta_pedestres} comparado ao ano anterior")
else:
    with col3:
        st.metric("Óbitos de Pedestres", total_pedestres)  # Passar total de pedestres
        st.markdown("<div style='color:orange; font-size: 14px; margin-top: -15px;'>Sem comparação</div>", unsafe_allow_html=True)

# Adicionar checkbox para exibir os dados brutos
exibir_dados_brutos = st.sidebar.checkbox("Exibir Dados Brutos")

# Exibir os dados brutos se o checkbox for marcado
if exibir_dados_brutos:
    st.subheader("Dados Brutos")
    st.write(data_filtrada)

def create_colored_bar_chart(data, x_column, y_column, title, color_column, color_scale):
    fig = px.bar(data, x=x_column, y=y_column, color=color_column, template='seaborn', color_continuous_scale=color_scale)
    fig.update_layout(
        title_text=title, 
        title_x=0, 
        margin=dict(l=0, r=10, b=10, t=30),
        yaxis_title=None, 
        xaxis_title=None,
        xaxis=dict(tickmode='linear', tick0=2019, dtick=1)
    )
    return fig

# Integração com a Mariaca AI
st.sidebar.header("Assistente de IA")
pergunta_usuario = st.sidebar.text_input("Faça uma pergunta sobre os dados:")

if st.sidebar.button("Enviar"):
    if pergunta_usuario:
        resposta_ia = obter_resposta_maritaca_ai(pergunta_usuario, data_filtrada)
        st.sidebar.write("**Resposta da IA:**")
        st.sidebar.write(resposta_ia)
    else:
        st.sidebar.write("Por favor, insira uma pergunta.")

col1, col2 = st.columns(2)

# Gráfico 1: Quantidade de Sinistros por Ano 
with col1:
    st.info("📊 Este gráfico mostra a quantidade de sinistros ao longo dos anos.")
    sinistros_por_ano = data_filtrada.groupby('Ano do BO').size().reset_index(name='Quantidade')
    fig1 = create_colored_bar_chart(sinistros_por_ano, x_column='Ano do BO', y_column='Quantidade', title='Quantidade de Sinistros por Ano', color_column='Quantidade', color_scale='Blues')
    st.plotly_chart(fig1, use_container_width=True)

# Gráfico 2: Quantidade de Vítimas Fatais por Ano 
with col2:
    st.info("📊 Este gráfico exibe o número de vítimas fatais por ano, auxiliando na análise de mudanças nas fatalidades.")
    vitimas_fatais_por_ano = data_filtrada.groupby('Ano do BO').size().reset_index(name='Vítimas Fatais')
    fig2 = create_colored_bar_chart(vitimas_fatais_por_ano, x_column='Ano do BO', y_column='Vítimas Fatais', title='Quantidade de Vítimas Fatais por Ano', color_column='Vítimas Fatais', color_scale='Reds')
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)

# Gráfico 3: Distribuição de Sinistros por Dia da Semana 
with col3:
    st.info("📅 Este gráfico mostra a distribuição dos sinistros fatais em diferentes dias da semana.")
    sinistros_por_dia_semana = data_filtrada.groupby('Dia da Semana').size().reset_index(name='Quantidade')
    fig3 = create_colored_bar_chart(sinistros_por_dia_semana, x_column='Dia da Semana', y_column='Quantidade', title='Distribuição de Sinistros por Dia da Semana', color_column='Quantidade', color_scale='Greens')
    st.plotly_chart(fig3, use_container_width=True)

# Gráfico 4: Distribuição de Sinistros por Tipo de Veículo 
with col4:
    st.info("🚗 Este gráfico apresenta os tipos de veículos mais envolvidos em sinistros fatais.")
    sinistros_por_veiculo = data_filtrada.groupby('Meio de locomocao da vitima').size().reset_index(name='Quantidade')
    fig4 = create_colored_bar_chart(sinistros_por_veiculo, x_column='Meio de locomocao da vitima', y_column='Quantidade', title='Distribuição de Sinistros por Tipo de Veículo', color_column='Quantidade', color_scale='Oranges')
    st.plotly_chart(fig4, use_container_width=True)

col5, col6 = st.columns(2)

# Gráfico 5: Comparação de Gênero x Horário do Sinistro 
with col5:
    st.info("🕒 Compare a ocorrência de sinistros fatais por gênero e horário do dia.")
    if 'Hora do Sinistro' in data_filtrada.columns and 'Sexo' in data_filtrada.columns:
        # Converter 'Hora do Sinistro' para numérico, tratando erros
        data_filtrada['Hora do Sinistro'] = pd.to_numeric(data_filtrada['Hora do Sinistro'], errors='coerce')
        genero_horario = data_filtrada.groupby(['Sexo', 'Hora do Sinistro']).size().reset_index(name='Quantidade')
        fig5 = px.line(genero_horario, x='Hora do Sinistro', y='Quantidade', color='Sexo', 
                       title='Comparação de Gênero x Horário do Sinistro', 
                       labels={'Quantidade':'Número de Sinistros', 'Hora do Sinistro':'Horário'},
                       template='seaborn')

        fig5.update_layout(
            title_x=0,
            margin=dict(l=0, r=10, b=10, t=30),
            xaxis_title='Horário do Dia',
            yaxis_title='Número de Sinistros',
            legend_title_text='Gênero'
        )
        
        st.plotly_chart(fig5, use_container_width=True)
    else:
        st.write("Colunas 'Hora do Sinistro' ou 'Gênero' não encontradas nos dados.")

# Gráfico 6: Turno com Maior Incidência de Sinistros 
with col6:
    st.info("⏳ Veja em quais turnos do dia ocorrem mais sinistros fatais.")
    def classificar_turno(hora):
        if pd.isna(hora):
            return 'Desconhecido'
        if 6 <= hora < 12:
            return 'Manhã'
        elif 12 <= hora < 18:
            return 'Tarde'
        elif 18 <= hora < 24:
            return 'Noite'
        else:
            return 'Madrugada'

    if 'Hora do Sinistro' in data_filtrada.columns:
        data_filtrada['Turno'] = data_filtrada['Hora do Sinistro'].apply(classificar_turno)
        sinistros_por_turno = data_filtrada.groupby('Turno').size().reset_index(name='Quantidade')
        fig6 = create_colored_bar_chart(sinistros_por_turno, x_column='Turno', y_column='Quantidade', title='Turno com Maior Incidência de Sinistros', color_column='Quantidade', color_scale='YlOrBr')
        st.plotly_chart(fig6, use_container_width=True)
    else:
        st.write("Coluna 'Hora do Sinistro' não encontrada nos dados.")

col7, col8 = st.columns(2)

# Gráfico 7: Distribuição de Óbitos por Faixa Etária 
with col7:
    st.info("👶👵 Este gráfico exibe a distribuição de óbitos fatais de acordo com a faixa etária.")
    if 'Faixa etaria' in data_filtrada.columns:
        faixa_etaria = data_filtrada.groupby('Faixa etaria').size().reset_index(name='Quantidade')
        fig7 = create_colored_bar_chart(faixa_etaria, x_column='Faixa etaria', y_column='Quantidade', title='Distribuição de Óbitos por Faixa Etária', color_column='Quantidade', color_scale='Blues')
        st.plotly_chart(fig7, use_container_width=True)
    else:
        st.write("Coluna 'Faixa etaria' não encontrada nos dados.")

# Gráfico 8: Óbitos por Tipo de Via 
with col8:
    st.info("🚧 Visualize os tipos de vias mais associados a óbitos fatais.")
    if 'Tipo de Via' in data_filtrada.columns:
        tipo_via = data_filtrada.groupby('Tipo de Via').size().reset_index(name='Quantidade')
        fig8 = create_colored_bar_chart(tipo_via, x_column='Tipo de Via', y_column='Quantidade', title='Óbitos por Tipo de Via', color_column='Quantidade', color_scale='Reds')
        st.plotly_chart(fig8, use_container_width=True)
    else:
        st.write("Coluna 'Tipo de Via' não encontrada nos dados.")

col9, col10 = st.columns(2)

# Gráfico 10: Óbitos por Sexo 
with col10:
    st.info("👫 Compare o número de óbitos fatais por sexo.")
    if 'Sexo' in data_filtrada.columns:
        obitos_por_sexo = data_filtrada.groupby('Sexo').size().reset_index(name='Quantidade')
        fig10 = create_colored_bar_chart(obitos_por_sexo, x_column='Sexo', y_column='Quantidade', title='Óbitos por Gênero', color_column='Quantidade', color_scale='Greys')
        st.plotly_chart(fig10, use_container_width=True)
    else:
        st.write("Coluna 'Gênero' não encontrada nos dados.")

col11, col12 = st.columns(2)

# Gráfico 11: Óbitos por Mês do Ano
with col11:
    st.info("📅 Este gráfico mostra a distribuição de óbitos fatais ao longo dos meses do ano.")
    if 'Mes do Obito' in data_filtrada.columns:
        mes_do_ano = data_filtrada.groupby('Mes do Obito').size().reset_index(name='Quantidade')
        fig11 = create_colored_bar_chart(mes_do_ano, x_column='Mes do Obito', y_column='Quantidade', title='Óbitos por Mês do Ano', color_column='Quantidade', color_scale='BuGn')
        st.plotly_chart(fig11, use_container_width=True)
    else:
        st.write("Coluna 'Mes do Obito' não encontrada nos dados.")

# Gráfico 12: Óbitos por Dia do Mês
with col12:
    st.info("📆 Veja como os óbitos fatais se distribuem ao longo dos dias de cada mês.")
    if 'Dia do Obito' in data_filtrada.columns:
        dia_do_mes = data_filtrada.groupby('Dia do Obito').size().reset_index(name='Quantidade')
        fig12 = create_colored_bar_chart(dia_do_mes, x_column='Dia do Obito', y_column='Quantidade', title='Óbitos por Dia do Mês', color_column='Quantidade', color_scale='YlGnBu')
        st.plotly_chart(fig12, use_container_width=True)
    else:
        st.write("Coluna 'Dia do Obito' não encontrada nos dados.")

# Lista de Contatos Úteis
with st.expander("Contatos Úteis"):
    st.markdown("""
    ### Contatos Importantes para Segurança Viária em SP:
    
    - **Infosiga SP**
        - Telefone: (11) 3311-3000
        - Site: [Infosiga SP](https://www.infosiga.sp.gov.br)
    
    - **Secretaria de Trânsito do Estado de SP**
        - Telefone: (11) 3311-3000
    
    - **Polícia Militar**
        - Telefone: 190
    
    - **Corpo de Bombeiros**
        - Telefone: 193
    
    - **SAMU (Serviço de Atendimento Móvel de Urgência)**
        - Telefone: 192
    
    - **DER (Departamento de Estradas de Rodagem)**
        - Telefone: 0800-055-5510
    
    - **CET (Companhia de Engenharia de Tráfego)**
        - Telefone: 1188
    """)
