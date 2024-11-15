import re
import time
import streamlit as st
import pandas as pd
import plotly.express as px
import maritalk
import os
from dotenv import load_dotenv
from PIL import Image
Image.MAX_IMAGE_PIXELS = None  # Isso desativa a proteção contra "Decompression Bomb"

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Carregar a chave da API Maritaca
MARITACA_API_KEY = st.secrets["MARITACA_API_KEY"]
#MARITACA_API_KEY = os.getenv("MARITACA_API_KEY")
# Configuração da página
st.set_page_config(page_title='Análise de Óbitos em Franca/SP', layout='wide', page_icon=':bar_chart:')

def load_data():
    data = pd.read_csv('obitos_final_nov.csv', delimiter=';')
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
    contexto = f"A faixa etária mais afetada por acidentes é {faixa_etaria_mais_afetada}, com {total} óbitos."
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
    contexto = f"O tipo de via com mais óbitos é {tipo_via_mais_obitos}, com {total} óbitos."
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
    contexto = f"O mês com mais acidentes é {mes_mais_acidentes}, com {total} acidentes."
    return contexto

def contexto_dia_mes_mais_acidentes(data):
    dia_mes_mais_acidentes = data['Dia do Sinistro'].value_counts().idxmax()
    total = data['Dia do Sinistro'].value_counts().max()
    contexto = f"O dia do mês com mais acidentes é {dia_mes_mais_acidentes}, com {total} acidentes."
    return contexto

def contexto_periodo_dia_mais_obitos(data):
    periodo_mais_obitos = data['Turno'].value_counts().idxmax()
    total = data['Turno'].value_counts().max()
    contexto = f"O período do dia com mais óbitos é {periodo_mais_obitos}, com {total} óbitos."
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

def contexto_distribuicao_obitos_por_tipo_vitima(data, pergunta):
    # Extrair o ano da pergunta
    match = re.search(r'em (\d{4})', pergunta)
    if match:
        ano = int(match.group(1))
        data_ano = data[data['Ano'] == ano]
        distribuicao = data_ano['Tipo de vitima'].value_counts().to_dict()
        contexto = f"Distribuição de óbitos por tipo de vítima em {ano}:\n"
        for tipo, total in distribuicao.items():
            contexto += f"{tipo}: {total} óbitos\n"
    else:
        contexto = "Por favor, especifique o ano para a análise."
    return contexto

# Dicionário de mapeamento de perguntas para funções
def contexto_default(data):
    return "Desculpe, não tenho informações para responder a essa pergunta."

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
    "Qual a distribuição de óbitos por tipo de vítima (condutor, passageiro, pedestre) em [ano]?": contexto_distribuicao_obitos_por_tipo_vitima,
}

# Função para obter resposta da Maritaca AI com o contexto gerado
def obter_resposta_maritaca_ai(pergunta, data):
    time.sleep(2)
    try:
        if pergunta in pergunta_para_funcao:
            funcao_contexto = pergunta_para_funcao[pergunta]
            if pergunta == "Qual a distribuição de óbitos por tipo de vítima (condutor, passageiro, pedestre) em [ano]?":
                contexto = funcao_contexto(data, pergunta)
            else:
                contexto = funcao_contexto(data)
        else:
            contexto = "Desculpe, não tenho informações para responder a essa pergunta."
        
        prompt = f"Contexto:\n{contexto}\n\nPergunta: {pergunta}\nResposta:"
        
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

# Sidebar content
st.sidebar.header("Informações Importantes")
with st.sidebar.expander("O que você precisa saber sobre os dados disponíveis para esta análise."):
    st.write(
        """
        Foram registrados **205 óbitos** no período de 2019 a 2023. Durante a análise, foram identificadas as seguintes lacunas nos dados:
        - **31 bairros não identificados**.
        - **9 óbitos** sem a informação sobre a **idade da vítima**.
        - **12 registros** sem informações sobre o **tipo de acidente** (atropelamento, choque, tombamento, etc.).
        - **6 casos** onde o **tipo de vítima** não foi informado (pedestre, motorista, etc.).
        - **2 registros** com o **meio de locomoção da vítima** não identificado.
        - **10 casos** com o **tipo de local do sinistro** não disponível.
        - **11 registros** com o **logradouro** não identificado.
        - **28 registros** sem informações sobre o **turno** do acidente.
        
        **Importante:** A ausência de informações em várias colunas pode comprometer a precisão e a profundidade das análises realizadas.
        
        Caso tenha dúvidas sobre a origem dos dados ou sobre o processo de tratamento e limpeza das informações, estamos à disposição para fornecer esclarecimentos detalhados.
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
    file_name="obitos_final_nov.csv",
    mime="text/csv",
)    

st.sidebar.header("Assistente de IA")
pergunta_selecionada = st.sidebar.selectbox(
    "Selecione uma pergunta:",
    [
        "Selecione uma pergunta...",  
        "Quantos óbitos ocorreram em 2021?",
        "Qual a faixa etária mais afetada por acidentes?",
        "Em qual bairro ocorreram mais óbitos?",
        "Qual o tipo de via com mais óbitos?",
        "Quantos óbitos ocorreram em cada dia da semana?",
        "Qual o horário com mais óbitos?",
        "Qual o sexo com mais acidentes?",
        "Qual o mês com mais acidentes?",
        "Qual o dia do mês com mais acidentes?",
        "Qual o período do dia com mais óbitos?",
        "Qual o meio de locomoção com mais óbitos?",
        "Quais os tipos de acidentes mais comuns?",
        "Qual a distribuição de óbitos por tipo de vítima (condutor, passageiro, pedestre) em [ano]?"
    ]
)

if st.sidebar.button("Enviar"):
    with st.sidebar:
        placeholder = st.empty()
        placeholder.write("Aguarde, processando a resposta...") 
        if pergunta_selecionada:
            resposta_ia = obter_resposta_maritaca_ai(pergunta_selecionada, data)
            placeholder.empty() 
            st.write("**Resposta da IA:**")
            st.write(resposta_ia)
        else:
            placeholder.empty() 
            st.write("Por favor, selecione uma pergunta.")

col1, col2 = st.columns([0.2, 0.8])  
with col1:
    st.image('images/escudo.png', width=100)  
with col2:
    st.title("Análise de Óbitos em Acidentes de Trânsito na Cidade de Franca/SP")
    st.markdown("Fonte dos Dados Brutos: [Infosiga SP](https://www.infosiga.sp.gov.br/?name=identificacao4&contextId=8a80809939587c0901395881fc2b0004)")
    st.markdown("Código Fonte: [GitHub](https://github.com/gabriellmelo/analise-exploratoria-tcc)")
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


# Métricas no topo
st.subheader("Insights")
col1, col2, col3 = st.columns(3)

# Total de óbitos
total_obitos = len(data_filtrada)

# Exibir os dados brutos se o checkbox for marcado
if exibir_dados_brutos:
    st.subheader("Dados Brutos")
    st.write(data_filtrada)

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
total_veiculos_motorizados = len(veiculos_motorizados)  

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
total_pedestres = len(pedestres)  

if ano_anterior is not None and not dados_ano_anterior.empty:
    pedestres_anterior = dados_ano_anterior[dados_ano_anterior['Meio de locomocao da vitima'] == 'PEDESTRE']
    delta_pedestres = total_pedestres - len(pedestres_anterior)
    col3.metric("Óbitos de Pedestres", total_pedestres, delta=f"{delta_pedestres} comparado ao ano anterior")
else:
    with col3:
        st.metric("Óbitos de Pedestres", total_pedestres)  # Passar total de pedestres
        st.markdown("<div style='color:orange; font-size: 14px; margin-top: -15px;'>Sem comparação</div>", unsafe_allow_html=True)

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
# Gráfico 1: Quantidade de Sinistros por Ano 
with col1:
    st.info("📊 Este gráfico mostra a quantidade de sinistros ao longo dos anos.")
    sinistros_por_ano = data_filtrada.groupby('Ano').size().reset_index(name='Quantidade')
    fig1 = create_colored_bar_chart(sinistros_por_ano, x_column='Ano', y_column='Quantidade', title='Quantidade de Sinistros por Ano', color_column='Quantidade', color_scale='Blues')
    st.plotly_chart(fig1, use_container_width=True)

# Gráfico 2: Distribuição de Óbitos por Tipo de Sinistro
with col2:
    st.info("🚧 Este gráfico exibe a distribuição de óbitos por tipo de sinistro.")
    obitos_por_tipo_sinistro = data_filtrada['Tipo de Sinistro'].value_counts().reset_index(name='Quantidade')
    obitos_por_tipo_sinistro = obitos_por_tipo_sinistro.rename(columns={'index': 'Tipo de Sinistro'})
    fig2 = create_colored_bar_chart(obitos_por_tipo_sinistro, x_column='Tipo de Sinistro', y_column='Quantidade', title='Distribuição de Óbitos por Tipo de Sinistro', color_column='Quantidade', color_scale='Reds')
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
    if 'Meio de locomocao da vitima' in data_filtrada.columns:
        # Remover dados "NAO DISPONIVEL"
        data_filtrada = data_filtrada[data_filtrada['Meio de locomocao da vitima'] != 'NAO DISPONIVEL']
        
        sinistros_por_veiculo = data_filtrada.groupby('Meio de locomocao da vitima').size().reset_index(name='Quantidade')
        fig4 = create_colored_bar_chart(sinistros_por_veiculo, x_column='Meio de locomocao da vitima', y_column='Quantidade', title='Distribuição de Sinistros por Tipo de Veículo', color_column='Quantidade', color_scale='Oranges')
        st.plotly_chart(fig4, use_container_width=True)
    else:
        st.write("Coluna 'Meio de locomocao da vitima' não encontrada nos dados.")

col5, col6 = st.columns(2)

# Gráfico 5: Comparação de Turno x Tipo de Via
with col5:
    st.info("🚧 Compare a ocorrência de sinistros fatais por turno do dia e tipo de via.")
    if 'Turno' in data_filtrada.columns and 'Tipo de Via' in data_filtrada.columns:
        data_filtrada = data_filtrada[(data_filtrada['Turno'] != 'NAO DISPONIVEL') & (data_filtrada['Tipo de Via'] != 'NAO DISPONIVEL')]
        
        turno_tipo_via = data_filtrada.groupby(['Turno', 'Tipo de Via']).size().reset_index(name='Quantidade')
        fig5 = px.bar(turno_tipo_via, x='Tipo de Via', y='Quantidade', color='Turno', 
                      title='Comparação de Turno x Tipo de Via', 
                      labels={'Quantidade':'Número de Sinistros', 'Tipo de Via':'Tipo de Via'},
                      template='seaborn')

        fig5.update_layout(
            title_x=0,
            margin=dict(l=0, r=10, b=10, t=30),
            xaxis_title='Tipo de Via',
            yaxis_title='Número de Sinistros',
            legend_title_text='Turno'
        )
        
        st.plotly_chart(fig5, use_container_width=True)
    else:
        st.write("Colunas 'Turno' ou 'Tipo de Via' não encontradas nos dados.")

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
        data_filtrada = data_filtrada[data_filtrada['Faixa etaria'] != 'NAO DISPONIVEL']
        
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

# Adicionar gráfico de barras para os 3 bairros com maiores índices de acidentes
with col9:
    st.info("🏘️ Este gráfico exibe os 3 bairros com maiores índices de acidentes.")
    if 'Bairro' in data_filtrada.columns:
        top3_bairros = data_filtrada['Bairro'].value_counts().reset_index(name='Quantidade')
        top3_bairros = top3_bairros.rename(columns={'index': 'Bairro'})
        top3_bairros = top3_bairros[top3_bairros['Bairro'] != 'Bairro não identificado'].head(3)
        if not top3_bairros.empty:
            fig_top3 = create_colored_bar_chart(top3_bairros, x_column='Bairro', y_column='Quantidade', title='Top 3 Bairros com Mais Acidentes', color_column='Quantidade', color_scale='Oranges')
            st.plotly_chart(fig_top3, use_container_width=True)
        else:
            st.write("Nenhum dado disponível para os bairros.")
    else:
        st.write("Coluna 'Bairro' não encontrada nos dados.")

# Gráfico 9: Óbitos por Sexo 
with col10:
    st.info("👫 Compare o número de óbitos fatais por gênero.")
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
    if 'Mes do Sinistro' in data_filtrada.columns:
        mes_do_ano = data_filtrada.groupby('Mes do Sinistro').size().reset_index(name='Quantidade')
        fig11 = create_colored_bar_chart(mes_do_ano, x_column='Mes do Sinistro', y_column='Quantidade', title='Acidentes por Mês do Ano', color_column='Quantidade', color_scale='BuGn')
        st.plotly_chart(fig11, use_container_width=True)
    else:
        st.write("Coluna 'Mes do Sinistro' não encontrada nos dados.")

# Gráfico 12: Óbitos por Dia do Mês
with col12:
    st.info("📆 Veja como os óbitos fatais se distribuem ao longo dos dias de cada mês.")
    if 'Dia do Sinistro' in data_filtrada.columns:
        dia_do_mes = data_filtrada.groupby('Dia do Sinistro').size().reset_index(name='Quantidade')
        fig12 = create_colored_bar_chart(dia_do_mes, x_column='Dia do Sinistro', y_column='Quantidade', title='Acidentes por Dia do Mês', color_column='Quantidade', color_scale='YlGnBu')
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