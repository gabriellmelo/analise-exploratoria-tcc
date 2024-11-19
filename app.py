import re
import time
import streamlit as st
import pandas as pd
import plotly.express as px
import maritalk
import os
from dotenv import load_dotenv
from PIL import Image
Image.MAX_IMAGE_PIXELS = None  

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Carregar a chave da API Maritaca
MARITACA_API_KEY = st.secrets["MARITACA_API_KEY"] # Para armazenar a chave no streamlit
#MARITACA_API_KEY = os.getenv("MARITACA_API_KEY") # Para uso local

# Configuração da página
st.set_page_config(page_title='Análise de Óbitos em Franca/SP', layout='wide', page_icon=':bar_chart:')

# Função para carregar os dados
def load_data():
    data = pd.read_csv('obitos_final.csv', delimiter=';')
    return data

data = load_data()

# Funções de contexto para cada pergunta
def contexto_obitos_2021(data):
    total_obitos = data[data['Ano'] == 2021].shape[0]
    contexto = f"No ano de 2021, ocorreram {total_obitos} óbitos em Franca."
    return contexto

def contexto_faixa_etaria_mais_afetada(data):
    faixa_etaria_mais_afetada = data['Faixa etaria'].value_counts().idxmax()
    total = data['Faixa etaria'].value_counts().max()
    contexto = f"A faixa etária mais afetada por acidentes é entre {faixa_etaria_mais_afetada}, com {total} óbitos."
    return contexto

def contexto_bairro_mais_obitos(data):
    data_bairro = data[data['Bairro'] != 'Bairro não identificado']
    if data_bairro.empty:
        contexto = "Não há dados disponíveis sobre os bairros identificados."
    else:
        bairro_mais_obitos = data_bairro['Bairro'].value_counts().idxmax()
        total = data_bairro['Bairro'].value_counts().max()
        contexto = f"O bairro com mais óbitos é {bairro_mais_obitos}, com {total} óbitos."
    return contexto

def contexto_tipo_via_mais_obitos(data):
    tipo_via_mais_obitos = data['Tipo de Via'].value_counts().idxmax()
    total = data['Tipo de Via'].value_counts().max()
    contexto = f"O tipo de via com mais óbitos são as {tipo_via_mais_obitos}, com {total} óbitos."
    return contexto

def contexto_obitos_por_dia_semana(data):
    obitos_por_dia = data['Dia da Semana'].value_counts().to_dict()
    contexto = "Número de óbitos por dia da semana:\n"
    for dia, total in obitos_por_dia.items():
        contexto += f"{dia}: {total} óbitos\n"
    return contexto

def contexto_horario_mais_obitos(data):
    horario_mais_obitos = data['Hora do Sinistro'].value_counts().idxmax()
    total = data['Hora do Sinistro'].value_counts().max()
    contexto = f"O horário com mais óbitos é às {horario_mais_obitos} horas, com {total} óbitos."
    return contexto

def contexto_sexo_mais_acidentes(data):
    sexo_mais_acidentes = data['Sexo'].value_counts().idxmax()
    total = data['Sexo'].value_counts().max()
    contexto = f"O sexo com mais acidentes é {sexo_mais_acidentes}, com {total} ocorrências."
    return contexto

def contexto_mes_mais_acidentes(data):
    mes_mais_acidentes = data['Mes do Sinistro'].value_counts().idxmax()
    total = data['Mes do Sinistro'].value_counts().max()
    contexto = f"O mês com mais acidentes é o mês {mes_mais_acidentes}, com {total} acidentes."
    return contexto

def contexto_dia_mes_mais_acidentes(data):
    dia_mes_mais_acidentes = data['Dia do Sinistro'].value_counts().idxmax()
    total = data['Dia do Sinistro'].value_counts().max()
    contexto = f"O dia do mês com mais acidentes é o dia {dia_mes_mais_acidentes}, com {total} acidentes."
    return contexto

def contexto_periodo_dia_mais_obitos(data):
    periodo_mais_obitos = data['Turno'].value_counts().idxmax()
    total = data['Turno'].value_counts().max()
    contexto = f"O período do dia com mais óbitos é o período da {periodo_mais_obitos}, com {total} óbitos."
    return contexto

def contexto_meio_locomocao_mais_obitos(data):
    meio_locomocao_mais_obitos = data['Meio de locomocao da vitima'].value_counts().idxmax()
    total = data['Meio de locomocao da vitima'].value_counts().max()
    contexto = f"O meio de locomoção com mais óbitos é {meio_locomocao_mais_obitos}, com {total} óbitos."
    return contexto

def contexto_tipos_acidentes_mais_comuns(data):
    tipos_acidentes = data['Tipo de Sinistro'].value_counts().head(5).to_dict()
    contexto = "Os tipos de acidentes mais comuns são:\n"
    for tipo, total in tipos_acidentes.items():
        contexto += f"{tipo}: {total} ocorrências\n"
    return contexto

def contexto_comparativo_obitos_por_mes(data):
    obitos_por_mes_ano = data.groupby(['Mes do Sinistro', 'Ano']).size().unstack().T.fillna(0)
    
    picos_obitos = {}
    for mes, anos in obitos_por_mes_ano.iterrows():
        mes_max = anos.idxmax()  
        picos_obitos[mes] = f"{mes_max} - {int(anos[mes_max])} óbitos"
    
    contexto = "Meses com os maiores picos de óbitos por ano:\n"
    for mes, resultado in picos_obitos.items():
        contexto += f"{mes}: {resultado}\n"
    
    return contexto

def contexto_media_obitos_por_bairro(data):
    obitos_por_bairro = data.groupby('Bairro').size()
    media_obitos = round(obitos_por_bairro.mean())
    contexto = f"A média de óbitos por bairro é de {media_obitos} óbitos por bairro."
    return contexto

def contexto_proporcao_obitos_por_tipo_vitima(data):
    tipos_vitima = data['Tipo de vitima'].value_counts(normalize=True) * 100
    contexto = "Proporção de óbitos por tipo de vítima (em %):\n"
    for tipo, proporcao in tipos_vitima.items():
        contexto += f"{tipo}: {proporcao:.2f}%\n"
    return contexto

def contexto_idade_media_vitimas(data):
    idade_media = round(data['Idade da vitima'].mean())
    contexto = f"A idade média das vítimas de acidentes de trânsito é de {idade_media} anos."
    return contexto

def contexto_comparativo_dezembro_janeiro(data):
    meses_comparados = data[data['Mes do Sinistro'].isin([12, 1])]
    obitos_dezembro_janeiro = meses_comparados.groupby(['Ano', 'Mes do Sinistro']).size().unstack(fill_value=0)
    if obitos_dezembro_janeiro.empty:
        return "Não há dados suficientes para comparar os óbitos entre dezembro e janeiro nos anos de 2019 a 2023."
    
    contexto = "Comparativo de óbitos entre dezembro e janeiro (2019-2023):\n"
    resumo = [] 
    for ano, meses in obitos_dezembro_janeiro.iterrows():
        dezembro = meses[12]
        janeiro = meses[1]
        delta = janeiro - dezembro
        contexto += f"Ano: {ano} - Dezembro: {dezembro} óbitos, Janeiro: {janeiro} óbitos - Diferença: {delta} óbitos\n"
        resumo.append(f"{ano}: {delta} óbitos")

    insight = """
    Embora os meses de dezembro e janeiro sejam frequentemente associados a festividades e férias, os dados indicam uma variação nos óbitos ao longo dos anos. 
    Nos últimos dois anos (2022 e 2023), houve uma leve redução, embora não muito expressiva. Em contraste, 2020 e 2021 registraram um aumento no número de óbitos. 
    Esse padrão sugere uma tendência de estabilização nas ocorrências de óbitos durante esse período, com uma diminuição gradual ao longo dos últimos anos, apesar das 
    festividades típicas desse período.
    """
    resumo_sucinto = f"\nResumo: {', '.join(resumo)}"
    return contexto + insight + resumo_sucinto

def obter_resposta_maritaca_ai(pergunta, data):
    # Gerar o contexto com base na pergunta
    contexto = pergunta_para_funcao.get(pergunta)(data)
    # Preparar o prompt para a Maritaca AI
    prompt = f"{contexto}\n\nCom base nas informações acima, responda à seguinte pergunta:\n{pergunta}\nResposta:"

    # Fazer a chamada para a Maritaca AI
    try:
        # Configurar o modelo Maritaca AI
        model = maritalk.MariTalk(
            key=MARITACA_API_KEY,
            model="sabia-3"
        )

        response = model.generate(prompt, max_tokens=500)
        answer = response["answer"]

        return answer
    except Exception as e:
        return f"Erro ao conectar com a API: {e}"
    
pergunta_para_funcao = {
    "Quantos óbitos ocorreram em 2021?": contexto_obitos_2021,
    "Qual a faixa etária mais afetada por acidentes?": contexto_faixa_etaria_mais_afetada,
    "Em qual bairro ocorreram mais óbitos?": contexto_bairro_mais_obitos,
    "Qual o tipo de via com mais óbitos?": contexto_tipo_via_mais_obitos,
    "Quantos óbitos ocorreram em cada dia da semana?": contexto_obitos_por_dia_semana,
    "Qual o horário com mais óbitos?": contexto_horario_mais_obitos,
    "Qual o sexo com mais acidentes?": contexto_sexo_mais_acidentes,
    "Qual o mês com mais acidentes?": contexto_mes_mais_acidentes,
    "Qual o dia do mês com mais acidentes?": contexto_dia_mes_mais_acidentes,
    "Qual o período do dia com mais óbitos?": contexto_periodo_dia_mais_obitos,
    "Qual o meio de locomoção com mais óbitos?": contexto_meio_locomocao_mais_obitos,
    "Quais os tipos de acidentes mais comuns?": contexto_tipos_acidentes_mais_comuns,
    "Em quais meses ocorrem mais óbitos em comparação com outros anos?": contexto_comparativo_obitos_por_mes,
    "Qual a média de óbitos por bairro?": contexto_media_obitos_por_bairro,
    "Qual a proporção de óbitos por tipo de vítima (condutor, passageiro, pedestre)?": contexto_proporcao_obitos_por_tipo_vitima,
    "Qual a idade média das vítimas de acidentes de trânsito?": contexto_idade_media_vitimas,
    "Como foi o comparativo de óbitos entre dezembro e janeiro nos anos de 2019 a 2023?": contexto_comparativo_dezembro_janeiro
}

# Sidebar 
st.sidebar.header("Informações Importantes")
with st.sidebar.expander("O que você precisa saber sobre os dados disponíveis para esta análise."):
    st.write(
        """
        Foram registrados **205 óbitos** no período de 2019 a 2023. Durante a análise, foram identificadas as seguintes lacunas nos dados:
        - **29 bairros não identificados**.
        - **11 logradouros não disponíveis**.
        - **9 óbitos** sem a informação sobre a **idade da vítima**.
        - **12 registros** sem informações sobre o **tipo de acidente** (atropelamento, choque, tombamento, etc.).
        - **6 casos** onde o **tipo de vítima** não foi informado (pedestre, motorista, etc.).
        - **2 registros** com o **meio de locomoção da vítima** não identificado.
        - **10 casos** com o **tipo de local do sinistro** não disponível.
        - **11 registros** com o **logradouro** não identificado.
        - **28 registros** sem informações sobre o **turno** do acidente.
        
        **Importante:** A ausência de informações em várias colunas pode comprometer a precisão das análises realizadas.
        
        Caso tenha dúvidas sobre a origem dos dados ou sobre o processo de tratamento e limpeza das informações, estamos à disposição para fornecer esclarecimentos detalhados.
        
        Para mais informações, entre em contato conosco através dos seguintes e-mails:
        - contato@gabrielmelo.com
        - gabrielfreitas034@gmail.com
        """
    )
st.sidebar.markdown("---") 

# Sidebar para filtro de ano
st.sidebar.header("Filtrar por Ano")
anos_disponiveis = [2019, 2020, 2021, 2022, 2023]
ano_selecionado = st.sidebar.selectbox("Escolha o Ano", ["Todos"] + [str(ano) for ano in anos_disponiveis], index=0)

# Carregar os dados e filtrar entre os anos de 2019 a 2023
data = data[data['Ano'].isin([2019, 2020, 2021, 2022, 2023])]

# Filtrar os dados de acordo com o ano selecionado
if ano_selecionado != "Todos":
    ano_selecionado = int(ano_selecionado)
    data_filtrada = data.loc[data['Ano'] == ano_selecionado]
else:
    data_filtrada = data

# Definir o ano anterior para cálculo dos deltas
if ano_selecionado != "Todos" and ano_selecionado > 2019:
    ano_anterior = ano_selecionado - 1
    dados_ano_anterior = data[data['Ano'] == ano_anterior]
else:
    ano_anterior = None
    dados_ano_anterior = pd.DataFrame()

# Adicionar checkbox para exibir os dados brutos
exibir_dados_brutos = st.sidebar.checkbox("Exibir Dados Brutos")

# Função para converter DataFrame em CSV
@st.cache_data
def convert_df(df):
    return df.to_csv().encode("utf-8")

csv = convert_df(data_filtrada)

# Botão de download na sidebar
st.sidebar.download_button(
    label="Dados disponíveis para download em CSV",
    data=csv,
    file_name="obitos_final.csv",
    mime="text/csv",
)    

st.sidebar.header("Assistente de IA")
pergunta_selecionada = st.sidebar.selectbox(
    "Selecione uma pergunta:",
    [
        "Selecione uma pergunta...",  
        "Quantos óbitos ocorreram em 2021?",
        "Como foi o comparativo de óbitos entre dezembro e janeiro nos anos de 2019 a 2023?",
        "Qual a faixa etária mais afetada por acidentes?",
        "Em qual bairro ocorreram mais óbitos?",
        "Qual a proporção de óbitos por tipo de vítima (condutor, passageiro, pedestre)?",
        "Qual o tipo de via com mais óbitos?",
        "Quantos óbitos ocorreram em cada dia da semana?",
        "Qual o horário com mais óbitos?",
        "Qual o sexo com mais acidentes?",
        "Qual o mês com mais acidentes?",
        "Qual o dia do mês com mais acidentes?",
        "Qual o período do dia com mais óbitos?",
        "Qual o meio de locomoção com mais óbitos?",
        "Quais os tipos de acidentes mais comuns?",
        "Em quais meses ocorrem mais óbitos em comparação com outros anos?", 
        "Qual a média de óbitos por bairro?",  
        "Qual a idade média das vítimas de acidentes de trânsito?", 
    ]
)

if st.sidebar.button("Enviar"):
    with st.sidebar:
        placeholder = st.empty()
        placeholder.write("Aguarde, processando a resposta...") 
        if pergunta_selecionada:
            resposta_ia = obter_resposta_maritaca_ai(pergunta_selecionada, data_filtrada)
            placeholder.empty() 
            st.write("**Resposta da IA:**")
            st.write(resposta_ia)
        else:
            placeholder.empty() 
            st.write("Por favor, selecione uma pergunta.")


col1, col2 = st.columns([0.15, 0.80])  

with col1:
    st.image('images/escudo.png', use_column_width=True)     
with col2:
    st.title("*Estatísticas de Óbitos em Acidentes de Trânsito em Franca*", help="Dados de 2019 a 2023")
    st.markdown(":bar_chart: **Fonte dos Dados Brutos**: [Infosiga SP](https://www.infosiga.sp.gov.br/?name=identificacao4&contextId=8a80809939587c0901395881fc2b0004)")
    st.markdown(":computer: **Código Fonte**: [GitHub](https://github.com/gabriellmelo/analise-exploratoria-tcc)")
    st.markdown(":calendar: **Data de Atualização**: 18/11/2024")
    
    st.markdown("---")

# Seção de Objetivo
st.markdown("""
    Esta aplicação tem como objetivo **:blue-background[analisar os dados de óbitos]** decorrentes de acidentes de trânsito na cidade de Franca nos últimos 5 anos, utilizando técnicas de análise de dados para:
    - **:blue-background[Identificar padrões e tendências]** que possam apoiar a formulação de **:blue-background[medidas preventivas]**;
    - **Contribuir para a melhoria da :blue-background[segurança viária]**;
    - **:blue-background[Democratizar o acesso a informações]**, facilitando o entendimento por **:blue-background[cidadãos]** e **:blue-background[autoridades locais]**.
""")
st.markdown("O projeto está alinhado com os [Objetivos de Desenvolvimento Sustentável (ODS)](https://brasil.un.org/pt-br/sdgs) da ONU, em especial o [Objetivo 11](https://www.ipea.gov.br/ods/ods11.html) - Cidades e Comunidades Sustentáveis.")

# Insights Section
st.subheader(":bar_chart: Visão Comparativa dos Óbitos por Acidente de Trânsito")

col1, col2, col3 = st.columns(3)

# Contagem total de óbitos
total_obitos = len(data_filtrada)

# Exibir os dados brutos se o checkbox for marcado
if exibir_dados_brutos:
    st.subheader(":clipboard: Dados Brutos")
    st.write(data_filtrada)

# Comparando com o ano anterior
if ano_anterior is not None and not dados_ano_anterior.empty:
    total_obitos_anterior = len(dados_ano_anterior)
    delta_obitos = total_obitos - total_obitos_anterior
    col1.metric(":coffin: Total de Óbitos", total_obitos, delta=f"{delta_obitos} comparado ao ano anterior", help="Total de óbitos")
else:
    with col1:
        st.metric(":coffin: Total de Óbitos", total_obitos)
        st.markdown("<div style='color:orange; font-size: 14px; margin-top: -15px;'>Sem comparação</div>", unsafe_allow_html=True)

# Óbitos por Motoristas e Condutores
motoristas_condutores = data_filtrada[data_filtrada['Tipo de vitima'].isin(['CONDUTOR', 'PASSAGEIRO'])]
total_motoristas_condutores = len(motoristas_condutores)

if ano_anterior is not None and not dados_ano_anterior.empty:
    motoristas_condutores_anterior = dados_ano_anterior[dados_ano_anterior['Tipo de vitima'].isin(['CONDUTOR', 'PASSAGEIRO'])]
    delta_motoristas_condutores = total_motoristas_condutores - len(motoristas_condutores_anterior)
    col2.metric(":car: Óbitos por Motoristas e Condutores", total_motoristas_condutores, delta=f"{delta_motoristas_condutores} comparado ao ano anterior", help="Óbitos envolvendo motoristas e condutores")
else:
    with col2:
        st.metric(":car: Óbitos por Motoristas e Condutores", total_motoristas_condutores)
        st.markdown("<div style='color:orange; font-size: 14px; margin-top: -15px;'>Sem comparação</div>", unsafe_allow_html=True)

# Óbitos de Pedestres
pedestres = data_filtrada[data_filtrada['Meio de locomocao da vitima'] == 'PEDESTRE']
total_pedestres = len(pedestres)

if ano_anterior is not None and not dados_ano_anterior.empty:
    pedestres_anterior = dados_ano_anterior[dados_ano_anterior['Meio de locomocao da vitima'] == 'PEDESTRE']
    delta_pedestres = total_pedestres - len(pedestres_anterior)
    col3.metric(":walking: Óbitos de Pedestres", total_pedestres, delta=f"{delta_pedestres} comparado ao ano anterior", help="Óbitos envolvendo pedestres em acidentes")
else:
    with col3:
        st.metric(":walking: Óbitos de Pedestres", total_pedestres)
        st.markdown("<div style='color:orange; font-size: 14px; margin-top: -15px;'>Sem comparação</div>", unsafe_allow_html=True)

# Função para criar gráfico de barras com cores gradientes
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

col1, col2 = st.columns(2)
# Gráfico 1: Quantidade de Acidentes por Ano 
with col1:
    st.info("📊 Este gráfico mostra a quantidade de acidentes ao longo dos anos.")
    sinistros_por_ano = data_filtrada.groupby('Ano').size().reset_index(name='Quantidade')
    fig1 = create_colored_bar_chart(sinistros_por_ano, x_column='Ano', y_column='Quantidade', title='Quantidade de Acidentes por Ano', color_column='Quantidade', color_scale='Blues')
    st.plotly_chart(fig1, use_container_width=True)

# Gráfico 2: Distribuição de Óbitos por Tipo de Sinistro
with col2:
    st.info("🚧 Este gráfico exibe a distribuição de óbitos por tipo de acidente.")
    obitos_por_tipo_sinistro = data_filtrada['Tipo de Sinistro'].value_counts().reset_index(name='Quantidade')
    obitos_por_tipo_sinistro = obitos_por_tipo_sinistro.rename(columns={'index': 'Tipo de Sinistro'})
    fig2 = create_colored_bar_chart(obitos_por_tipo_sinistro, x_column='Tipo de Sinistro', y_column='Quantidade', title='Distribuição de Óbitos por Tipo de Acidente', color_column='Quantidade', color_scale='Reds')
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)

# Gráfico 3: Distribuição de Acidentes por Dia da Semana 
with col3:
    st.info("📅 Este gráfico mostra a distribuição dos acidentes fatais em diferentes dias da semana.")
    sinistros_por_dia_semana = data_filtrada.groupby('Dia da Semana').size().reset_index(name='Quantidade')
    fig3 = create_colored_bar_chart(sinistros_por_dia_semana, x_column='Dia da Semana', y_column='Quantidade', title='Distribuição de Acidentes por Dia da Semana', color_column='Quantidade', color_scale='Greens')
    st.plotly_chart(fig3, use_container_width=True)

# Gráfico 4: Distribuição de Acidentes por Tipo de Veículo 
with col4:
    st.info("🚗 Este gráfico apresenta os tipos de veículos mais envolvidos em acidentes fatais.")
    if 'Meio de locomocao da vitima' in data_filtrada.columns:
        data_filtrada = data_filtrada[data_filtrada['Meio de locomocao da vitima'] != 'NAO DISPONIVEL']
        sinistros_por_veiculo = data_filtrada.groupby('Meio de locomocao da vitima').size().reset_index(name='Quantidade')
        fig4 = create_colored_bar_chart(sinistros_por_veiculo, x_column='Meio de locomocao da vitima', y_column='Quantidade', title='Distribuição de Acidentes por Tipo de Veículo', color_column='Quantidade', color_scale='Oranges')
        st.plotly_chart(fig4, use_container_width=True)
    else:
        st.write("Coluna 'Meio de locomocao da vitima' não encontrada nos dados.")

col5, col6 = st.columns(2)

# Gráfico 5: Comparação de Turno x Tipo de Via
with col5:
    st.info("🚧 Compare a ocorrência de acidentes fatais por turno do dia e tipo de via.")
    if 'Turno' in data_filtrada.columns and 'Tipo de Via' in data_filtrada.columns:
        data_filtrada = data_filtrada[(data_filtrada['Turno'] != 'NAO DISPONIVEL') & (data_filtrada['Tipo de Via'] != 'NAO DISPONIVEL')]
        
        turno_tipo_via = data_filtrada.groupby(['Turno', 'Tipo de Via']).size().reset_index(name='Quantidade')
        fig5 = px.bar(turno_tipo_via, x='Tipo de Via', y='Quantidade', color='Turno', 
                      title='Comparação de Turno x Tipo de Via', 
                      labels={'Quantidade':'Número de Acidentes', 'Tipo de Via':'Tipo de Via'},
                      template='seaborn')

        fig5.update_layout(
            title_x=0,
            margin=dict(l=0, r=10, b=10, t=30),
            xaxis_title='Tipo de Via',
            yaxis_title='Número de Acidentes',
            legend_title_text='Turno'
        )
        
        st.plotly_chart(fig5, use_container_width=True)
    else:
        st.write("Colunas 'Turno' ou 'Tipo de Via' não encontradas nos dados.")

# Gráfico 6: Turno com Maior Incidência de Acidentes 
with col6:
    st.info("⏳ Veja em quais turnos do dia ocorrem mais acidentes fatais.")
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
        fig6 = create_colored_bar_chart(sinistros_por_turno, x_column='Turno', y_column='Quantidade', title='Turno com Maior Incidência de Acidentes', color_column='Quantidade', color_scale='YlOrBr')
        st.plotly_chart(fig6, use_container_width=True)
    else:
        st.write("Coluna 'Hora do Sinistro' não encontrada nos dados.")

col7, col8 = st.columns(2)

# Gráfico 7: Distribuição de Óbitos por Faixa Etária 
with col7:
    st.info("👶👵 Este gráfico exibe a distribuição de acidentes fatais de acordo com a faixa etária.")
    if 'Faixa etaria' in data_filtrada.columns:
        data_filtrada = data_filtrada[data_filtrada['Faixa etaria'] != 'NAO DISPONIVEL']
        
        faixa_etaria = data_filtrada.groupby('Faixa etaria').size().reset_index(name='Quantidade')
        fig7 = create_colored_bar_chart(faixa_etaria, x_column='Faixa etaria', y_column='Quantidade', title='Distribuição de Óbitos por Faixa Etária', color_column='Quantidade', color_scale='Blues')
        st.plotly_chart(fig7, use_container_width=True)
    else:
        st.write("Coluna 'Faixa etaria' não encontrada nos dados.")

# Gráfico 8: Óbitos por Tipo de Via 
with col8:
    st.info("🚧 Visualize os tipos de vias mais associados a acidentes fatais.")
    if 'Tipo de Via' in data_filtrada.columns:
        tipo_via = data_filtrada.groupby('Tipo de Via').size().reset_index(name='Quantidade')
        fig8 = create_colored_bar_chart(tipo_via, x_column='Tipo de Via', y_column='Quantidade', title='Óbitos por Tipo de Via', color_column='Quantidade', color_scale='Reds')
        st.plotly_chart(fig8, use_container_width=True)
    else:
        st.write("Coluna 'Tipo de Via' não encontrada nos dados.")

col9, col10 = st.columns(2)

# 3 bairros com maiores índices de acidentes
with col9:
    st.info("🏘️ Este gráfico exibe os 3 bairros com maiores índices de acidentes.")
    if 'Bairro' in data_filtrada.columns:
        top3_bairros = data_filtrada['Bairro'].value_counts().reset_index(name='Quantidade')
        top3_bairros = top3_bairros.rename(columns={'index': 'Bairro'})
        top3_bairros = top3_bairros[top3_bairros['Bairro'] != 'Bairro não identificado'].head(3)
        if not top3_bairros.empty:
            fig_top3 = create_colored_bar_chart(top3_bairros, x_column='Bairro', y_column='Quantidade', title='Top 3 Bairros com Mais Acidentes', color_column='Quantidade', color_scale='Oranges')
            fig_top3.update_layout(
                yaxis=dict(
                    tickmode='linear',
                    dtick=1 
                )
            )
            st.plotly_chart(fig_top3, use_container_width=True)
        else:
            st.write("Nenhum dado disponível para os bairros.")
    else:
        st.write("Coluna 'Bairro' não encontrada nos dados.")

# Gráfico 9: Óbitos por Gênero 
with col10:
    st.info("👫 Compare o número de óbitos por gênero.")
    if 'Sexo' in data_filtrada.columns:
        obitos_por_sexo = data_filtrada.groupby('Sexo').size().reset_index(name='Quantidade')
        fig10 = create_colored_bar_chart(obitos_por_sexo, x_column='Sexo', y_column='Quantidade', title='Óbitos por Gênero', color_column='Quantidade', color_scale='Greys')
        st.plotly_chart(fig10, use_container_width=True)
    else:
        st.write("Coluna 'Gênero' não encontrada nos dados.")

col11, col12 = st.columns(2)

# Gráfico 11: Óbitos por Mês do Ano
with col11:
    st.info("📅 Este gráfico mostra a distribuição de óbitos ao longo dos meses do ano.")
    if 'Mes do Sinistro' in data_filtrada.columns:
        mes_do_ano = data_filtrada.groupby('Mes do Sinistro').size().reset_index(name='Quantidade')
        fig11 = create_colored_bar_chart(mes_do_ano, x_column='Mes do Sinistro', y_column='Quantidade', title='Acidentes por Mês do Ano', color_column='Quantidade', color_scale='BuGn')
        st.plotly_chart(fig11, use_container_width=True)
    else:
        st.write("Coluna 'Mes do Sinistro' não encontrada nos dados.")

# Gráfico 12: Óbitos por Dia do Mês
with col12:
    st.info("📆 Veja como os óbitos se distribuem ao longo dos dias de cada mês.")
    if 'Dia do Sinistro' in data_filtrada.columns:
        dia_do_mes = data_filtrada.groupby('Dia do Sinistro').size().reset_index(name='Quantidade')
        fig12 = create_colored_bar_chart(dia_do_mes, x_column='Dia do Sinistro', y_column='Quantidade', title='Acidentes por Dia do Mês', color_column='Quantidade', color_scale='YlGnBu')
        fig12.update_layout(
            yaxis=dict(
                tickmode='linear',
                dtick=1  
            )
        )
        st.plotly_chart(fig12, use_container_width=True)
    else:
        st.write("Coluna 'Dia do Sinistro' não encontrada nos dados.")

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