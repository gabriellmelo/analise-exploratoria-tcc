import pytest
import pandas as pd
import os
from dotenv import load_dotenv
from unittest.mock import patch, MagicMock
from app import detectar_tipo_pergunta, gerar_contexto, obter_resposta_maritaca_ai, load_data, create_colored_bar_chart, classificar_turno

# Teste para a função detectar_tipo_pergunta
def test_detectar_tipo_pergunta():
    assert detectar_tipo_pergunta("Qual é o ano?") == "ano"
    assert detectar_tipo_pergunta("Qual é a faixa etária?") == "faixa_etaria"
    assert detectar_tipo_pergunta("Qual é o dia da semana?") == "dia_semana"
    assert detectar_tipo_pergunta("Qualquer outra pergunta") == "geral"

# Teste para a função gerar_contexto
def test_gerar_contexto():
    data = pd.DataFrame({
        'Ano do BO': [2019, 2020, 2020, 2021],
        'Faixa etaria': ['0-10', '11-20', '21-30', '31-40'],
        'Dia da Semana': ['Segunda', 'Terça', 'Quarta', 'Quinta']
    })
    
    contexto_ano = gerar_contexto(data, "ano")
    assert "No ano de 2019, houve 1 óbitos." in contexto_ano
    assert "No ano de 2020, houve 2 óbitos." in contexto_ano
    assert "No ano de 2021, houve 1 óbitos." in contexto_ano
    
    contexto_faixa = gerar_contexto(data, "faixa_etaria")
    assert "Na faixa etária 0-10, houve 1 óbitos." in contexto_faixa
    assert "Na faixa etária 11-20, houve 1 óbitos." in contexto_faixa
    assert "Na faixa etária 21-30, houve 1 óbitos." in contexto_faixa
    assert "Na faixa etária 31-40, houve 1 óbitos." in contexto_faixa
    
    contexto_dia = gerar_contexto(data, "dia_semana")
    assert "No dia Segunda, houve 1 óbitos." in contexto_dia
    assert "No dia Terça, houve 1 óbitos." in contexto_dia
    assert "No dia Quarta, houve 1 óbitos." in contexto_dia
    assert "No dia Quinta, houve 1 óbitos." in contexto_dia

# Teste para a função obter_resposta_maritaca_ai
@patch('app.maritalk.MariTalk')
def test_obter_resposta_maritaca_ai(mock_maritalk):
    mock_model = MagicMock()
    mock_model.generate.return_value = {"answer": "Resposta mockada"}
    mock_maritalk.return_value = mock_model
    
    data = pd.DataFrame({
        'Ano do BO': [2019, 2020, 2020, 2021],
        'Faixa etaria': ['0-10', '11-20', '21-30', '31-40'],
        'Dia da Semana': ['Segunda', 'Terça', 'Quarta', 'Quinta']
    })
    
    resposta = obter_resposta_maritaca_ai("Qual é o ano?", data)
    assert resposta == "Resposta mockada"

# Teste para a função load_data
@patch('pandas.read_excel')
def test_load_data(mock_read_excel):
    mock_df = pd.DataFrame({
        'Ano do BO': [2019, 2020],
        'Faixa etaria': ['0-10', '11-20']
    })
    mock_read_excel.return_value = mock_df
    
    data = load_data()
    assert not data.empty
    assert 'Ano do BO' in data.columns
    assert 'Faixa etaria' in data.columns

# Teste para a função create_colored_bar_chart
def test_create_colored_bar_chart():
    data = pd.DataFrame({
        'Ano do BO': [2019, 2020, 2021],
        'Quantidade': [10, 20, 30]
    })
    fig = create_colored_bar_chart(data, x_column='Ano do BO', y_column='Quantidade', title='Teste', color_column='Quantidade', color_scale='Blues')
    assert fig.layout.title.text == 'Teste'
    assert fig.data[0].x.tolist() == [2019, 2020, 2021]
    assert fig.data[0].y.tolist() == [10, 20, 30]

# Teste para a função classificar_turno
def test_classificar_turno():
    assert classificar_turno(5) == 'Madrugada'
    assert classificar_turno(6) == 'Manhã'
    assert classificar_turno(12) == 'Tarde'
    assert classificar_turno(18) == 'Noite'
    assert classificar_turno(23) == 'Noite'

    # Teste para a função detectar_tipo_pergunta
    def test_detectar_tipo_pergunta():
        assert detectar_tipo_pergunta("Qual é o ano?") == "ano"
        assert detectar_tipo_pergunta("Qual é a faixa etária?") == "faixa_etaria"
        assert detectar_tipo_pergunta("Qual é o dia da semana?") == "dia_semana"
        assert detectar_tipo_pergunta("Qualquer outra pergunta") == "geral"

    # Teste para a função gerar_contexto
    def test_gerar_contexto():
        data = pd.DataFrame({
            'Ano do BO': [2019, 2020, 2020, 2021],
            'Faixa etaria': ['0-10', '11-20', '21-30', '31-40'],
            'Dia da Semana': ['Segunda', 'Terça', 'Quarta', 'Quinta']
        })
        
        contexto_ano = gerar_contexto(data, "ano")
        assert "No ano de 2019, houve 1 óbitos." in contexto_ano
        assert "No ano de 2020, houve 2 óbitos." in contexto_ano
        assert "No ano de 2021, houve 1 óbitos." in contexto_ano
        
        contexto_faixa = gerar_contexto(data, "faixa_etaria")
        assert "Na faixa etária 0-10, houve 1 óbitos." in contexto_faixa
        assert "Na faixa etária 11-20, houve 1 óbitos." in contexto_faixa
        assert "Na faixa etária 21-30, houve 1 óbitos." in contexto_faixa
        assert "Na faixa etária 31-40, houve 1 óbitos." in contexto_faixa
        
        contexto_dia = gerar_contexto(data, "dia_semana")
        assert "No dia Segunda, houve 1 óbitos." in contexto_dia
        assert "No dia Terça, houve 1 óbitos." in contexto_dia
        assert "No dia Quarta, houve 1 óbitos." in contexto_dia
        assert "No dia Quinta, houve 1 óbitos." in contexto_dia

    # Teste para a função obter_resposta_maritaca_ai
    @patch('app.maritalk.MariTalk')
    def test_obter_resposta_maritaca_ai(mock_maritalk):
        mock_model = MagicMock()
        mock_model.generate.return_value = {"answer": "Resposta mockada"}
        mock_maritalk.return_value = mock_model
        
        data = pd.DataFrame({
            'Ano do BO': [2019, 2020, 2020, 2021],
            'Faixa etaria': ['0-10', '11-20', '21-30', '31-40'],
            'Dia da Semana': ['Segunda', 'Terça', 'Quarta', 'Quinta']
        })
        
        resposta = obter_resposta_maritaca_ai("Qual é o ano?", data)
        assert resposta == "Resposta mockada"

    # Teste para a função load_data
    @patch('pandas.read_excel')
    def test_load_data(mock_read_excel):
        mock_df = pd.DataFrame({
            'Ano do BO': [2019, 2020],
            'Faixa etaria': ['0-10', '11-20']
        })
        mock_read_excel.return_value = mock_df
        
        data = load_data()
        assert not data.empty
        assert 'Ano do BO' in data.columns
        assert 'Faixa etaria' in data.columns

    # Teste para a função create_colored_bar_chart
    def test_create_colored_bar_chart():
        data = pd.DataFrame({
            'Ano do BO': [2019, 2020, 2021],
            'Quantidade': [10, 20, 30]
        })
        fig = create_colored_bar_chart(data, x_column='Ano do BO', y_column='Quantidade', title='Teste', color_column='Quantidade', color_scale='Blues')
        assert fig.layout.title.text == 'Teste'
        assert fig.data[0].x.tolist() == [2019, 2020, 2021]
        assert fig.data[0].y.tolist() == [10, 20, 30]

    # Teste para a função classificar_turno
    def test_classificar_turno():
        assert classificar_turno(5) == 'Madrugada'
        assert classificar_turno(6) == 'Manhã'
        assert classificar_turno(12) == 'Tarde'
        assert classificar_turno(18) == 'Noite'
        assert classificar_turno(23) == 'Noite'

    # Executar os testes
    if __name__ == "__main__":
        pytest.main()

# Executar os testes
if __name__ == "__main__":
    pytest.main()