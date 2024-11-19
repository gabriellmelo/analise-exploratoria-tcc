import pytest
import pandas as pd
from app import (
    load_data,
    contexto_obitos_2021,
    contexto_faixa_etaria_mais_afetada,
    contexto_bairro_mais_obitos,
    contexto_tipo_via_mais_obitos,
    contexto_obitos_por_dia_semana,
    contexto_horario_mais_obitos,
    contexto_sexo_mais_acidentes,
    contexto_mes_mais_acidentes,
    contexto_dia_mes_mais_acidentes,
    contexto_periodo_dia_mais_obitos,
    contexto_meio_locomocao_mais_obitos,
    contexto_tipos_acidentes_mais_comuns,
    contexto_distribuicao_obitos_por_tipo_vitima,
    contexto_default,
    obter_resposta_maritaca_ai,
    create_colored_bar_chart,
    classificar_turno
)
from unittest.mock import patch, MagicMock

def test_load_data():
    data = load_data()
    assert not data.empty
    # Verificar se as colunas esperadas estão presentes
    expected_columns = [
        'Ano', 'Faixa etaria', 'Dia da Semana', 'Bairro', 'Tipo de Via', 
        'Hora do Sinistro', 'Sexo', 'Mes do Sinistro', 'Dia do Sinistro', 
        'Turno', 'Meio de locomocao da vitima', 'Tipo de Sinistro', 
        'Tipo de vitima', 'Mes do Sinistro', 'Dia do Sinistro'
    ]
    for col in expected_columns:
        assert col in data.columns

def test_contexto_obitos_2021():
    data = pd.DataFrame({'Ano': [2021, 2021, 2020, 2019]})
    contexto = contexto_obitos_2021(data)
    assert contexto == "No ano de 2021, ocorreram 2 óbitos em Franca."

def test_contexto_faixa_etaria_mais_afetada():
    data = pd.DataFrame({'Faixa etaria': ['20-30', '20-30', '30-40', '40-50']})
    contexto = contexto_faixa_etaria_mais_afetada(data)
    assert contexto == "A faixa etária mais afetada por acidentes é 20-30, com 2 óbitos."

def test_contexto_bairro_mais_obitos():
    data = pd.DataFrame({'Bairro': ['Centro', 'Centro', 'Bairro não identificado', 'Vila Nova']})
    contexto = contexto_bairro_mais_obitos(data)
    assert contexto == "O bairro com mais óbitos é Centro, com 2 óbitos."

def test_contexto_tipo_via_mais_obitos():
    data = pd.DataFrame({'Tipo de Via': ['Rodovia', 'Avenida', 'Rodovia', 'Rua']})
    contexto = contexto_tipo_via_mais_obitos(data)
    assert contexto == "O tipo de via com mais óbitos é Rodovia, com 2 óbitos."

def test_contexto_obitos_por_dia_semana():
    data = pd.DataFrame({'Dia da Semana': ['Segunda-feira', 'Terça-feira', 'Segunda-feira', 'Quarta-feira']})
    contexto = contexto_obitos_por_dia_semana(data)
    expected = "Número de óbitos por dia da semana:\nSegunda-feira: 2 óbitos\nTerça-feira: 1 óbitos\nQuarta-feira: 1 óbitos\n"
    assert contexto == expected

def test_contexto_horario_mais_obitos():
    data = pd.DataFrame({'Hora do Sinistro': [10, 15, 10, 20]})
    contexto = contexto_horario_mais_obitos(data)
    assert contexto == "O horário com mais óbitos é às 10 horas, com 2 óbitos."

def test_contexto_sexo_mais_acidentes():
    data = pd.DataFrame({'Sexo': ['Masculino', 'Feminino', 'Masculino', 'Masculino']})
    contexto = contexto_sexo_mais_acidentes(data)
    assert contexto == "O sexo com mais acidentes é Masculino, com 3 ocorrências."

def test_contexto_mes_mais_acidentes():
    data = pd.DataFrame({'Mes do Sinistro': ['Janeiro', 'Fevereiro', 'Janeiro', 'Março']})
    contexto = contexto_mes_mais_acidentes(data)
    assert contexto == "O mês com mais acidentes é Janeiro, com 2 acidentes."

def test_contexto_dia_mes_mais_acidentes():
    data = pd.DataFrame({'Dia do Sinistro': [1, 2, 1, 3]})
    contexto = contexto_dia_mes_mais_acidentes(data)
    assert contexto == "O dia do mês com mais acidentes é 1, com 2 acidentes."

def test_contexto_periodo_dia_mais_obitos():
    data = pd.DataFrame({'Turno': ['Manhã', 'Tarde', 'Manhã', 'Noite']})
    contexto = contexto_periodo_dia_mais_obitos(data)
    assert contexto == "O período do dia com mais óbitos é Manhã, com 2 óbitos."

def test_contexto_meio_locomocao_mais_obitos():
    data = pd.DataFrame({'Meio de locomocao da vitima': ['Carro', 'Moto', 'Carro', 'Bicicleta']})
    contexto = contexto_meio_locomocao_mais_obitos(data)
    assert contexto == "O meio de locomoção com mais óbitos é Carro, com 2 óbitos."

def test_contexto_tipos_acidentes_mais_comuns():
    data = pd.DataFrame({'Tipo de Sinistro': ['Colisão', 'Atropelamento', 'Colisão', 'Tombamento', 'Colisão']})
    contexto = contexto_tipos_acidentes_mais_comuns(data)
    expected = "Os tipos de acidentes mais comuns são:\nColisão: 3 ocorrências\nAtropelamento: 1 ocorrências\nTombamento: 1 ocorrências\n"
    assert contexto == expected

def test_contexto_distribuicao_obitos_por_tipo_vitima():
    data = pd.DataFrame({
        'Ano': [2021, 2021, 2020, 2019],
        'Tipo de vitima': ['Condutor', 'Passageiro', 'Pedestre', 'Condutor']
    })
    pergunta = "Qual a distribuição de óbitos por tipo de vítima (condutor, passageiro, pedestre) em 2021?"
    contexto = contexto_distribuicao_obitos_por_tipo_vitima(data, pergunta)
    expected = "Distribuição de óbitos por tipo de vítima em 2021:\nCondutor: 1 óbitos\nPassageiro: 1 óbitos\n"
    assert contexto == expected

def test_contexto_default():
    data = pd.DataFrame()
    contexto = contexto_default(data)
    assert contexto == "Desculpe, não tenho informações para responder a essa pergunta."

@patch('app.maritalk.MariTalk')
def test_obter_resposta_maritaca_ai(mock_MariTalk):
    mock_model_instance = MagicMock()
    mock_model_instance.generate.return_value = {"answer": "Resposta mockada"}
    mock_MariTalk.return_value = mock_model_instance

    data = pd.DataFrame({'Ano': [2021, 2021, 2020, 2019]})
    pergunta = "Quantos óbitos ocorreram em 2021?"
    resposta = obter_resposta_maritaca_ai(pergunta, data)
    assert resposta == "Resposta mockada"

def test_create_colored_bar_chart():
    data = pd.DataFrame({
        'Ano': [2019, 2020, 2021],
        'Quantidade': [10, 20, 30],
        'Color': [1, 2, 3]
    })
    fig = create_colored_bar_chart(
        data, 
        x_column='Ano', 
        y_column='Quantidade', 
        title='Teste', 
        color_column='Color', 
        color_scale='Blues'
    )
    assert fig.layout.title.text == 'Teste'
    assert fig.data[0].x.tolist() == [2019, 2020, 2021]
    assert fig.data[0].y.tolist() == [10, 20, 30]

def test_classificar_turno():
    assert classificar_turno(5) == 'Madrugada'
    assert classificar_turno(6) == 'Manhã'
    assert classificar_turno(12) == 'Tarde'
    assert classificar_turno(18) == 'Noite'
    assert classificar_turno(23) == 'Noite'
    assert classificar_turno(None) == 'Desconhecido'

if __name__ == "__main__":
    pytest.main()