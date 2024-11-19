# Análise de Óbitos em Franca/SP

![Escudo de Franca](images/escudo.png)

## Visão Geral

Este projeto consiste em uma aplicação interativa desenvolvida com Streamlit para analisar dados de óbitos em acidentes de trânsito na cidade de Franca, São Paulo. Através de visualizações dinâmicas e filtros intuitivos, os usuários podem explorar diversas métricas relacionadas aos acidentes, como quantidade de óbitos por ano, distribuição por dia da semana, tipo de veículo envolvido, faixa etária das vítimas, entre outros.

Além disso, o projeto conta com a integração da API Maritaca AI, permitindo que os usuários selecionem perguntas pré-definidas sobre os dados analisados e recebam respostas automatizadas baseadas no contexto dos dados carregados.

Também incluímos um script adicional, `gmaps.py`, que pode ser usado para converter coordenadas geográficas em informações de logradouro e bairro utilizando a API do Google Maps, com uma interface construída em Streamlit.

### 📊 Funcionalidades

- **Dashboard Interativo**: Visualizações gráficas interativas utilizando Plotly Express.
- **Filtros Dinâmicos**: Filtragem de dados por ano para uma análise mais focada.
- **Diversas Métricas**:
    - Quantidade de óbitos por ano.
    - Distribuição de óbitos por tipo de sinistro.
    - Distribuição de acidentes por dia da semana.
    - Distribuição de acidentes por tipo de veículo.
    - Comparação de turno x tipo de via.
    - Turno com maior incidência de acidentes.
    - Distribuição de óbitos por faixa etária.
    - Óbitos por tipo de via.
    - Top 3 bairros com mais acidentes.
    - Óbitos por gênero.
    - Óbitos por mês do ano.
    - Óbitos por dia do mês.
- **Assistente de IA**: Integração com a API Maritaca AI para responder perguntas pré-definidas baseadas nos dados carregados.
- **Conversor de Coordenadas**: O script `gmaps.py` permite converter coordenadas de latitude e longitude em informações de logradouro e bairro usando a API do Google Maps, com interface via Streamlit.
- **Testes Unitários**: O arquivo `test_app.py` contém testes unitários para validar as funcionalidades da aplicação principal.
- **Download de Dados**: Os dados utilizados estão disponíveis para download em formato CSV.
- **Contatos Úteis**: Lista de contatos importantes para segurança viária em SP.
  
### 🚀 Tecnologias Utilizadas

- Python 3.8+
- Streamlit: Para construção da interface web interativa.
- Pandas: Manipulação e análise de dados.
- Plotly Express: Criação de visualizações gráficas.
- Maritaca AI: Integração de IA para responder perguntas automatizadas sobre o dataset.
- Google Maps API: Para conversão de coordenadas em logradouro e bairro.
- OpenPyXL: Leitura de arquivos Excel.
- Pytest: Para testes unitários.
- dotenv: Para gerenciamento de variáveis de ambiente.

## 📥 Instalação

### 1. Clone o Repositório

```bash
git clone https://github.com/gabriellmelo/analise-exploratoria-tcc.git
cd analise-exploratoria-tcc
```

### 2. Crie um Ambiente Virtual (Opcional, mas Recomendado)

```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

### 3. Instale as Dependências

```bash
pip install -r requirements.txt
```

> **Nota**: Se o arquivo `requirements.txt` não estiver disponível, você pode instalar as dependências manualmente:

```bash
pip install streamlit pandas plotly openpyxl python-dotenv maritalk requests
```

### 4. Configuração das Chaves de API

Crie um arquivo `.env` na raiz do projeto e adicione as suas chaves de API:

```bash
MARITACA_API_KEY='sua_chave_api_maritaca'
GOOGLE_MAPS_API_KEY='sua_chave_api_google_maps'
```

## 🗂️ Estrutura do Projeto

```
analise-exploratoria-tcc/
├── images/
│   └── escudo.png
├── obitos_final.csv
├── app.py
├── gmaps.py
├── test_app.py
├── README.md
├── .env
└── requirements.txt
```

- **images/**: Diretório contendo imagens utilizadas na aplicação.
- **obitos_final.csv**: Arquivo CSV com os dados de óbitos em Franca.
- **app.py**: Código fonte da aplicação Streamlit principal.
- **gmaps.py**: Script para conversão de coordenadas em logradouro e bairro usando a API do Google Maps com Streamlit.
- **test_app.py**: Arquivo de testes unitários para a aplicação principal.
- **README.md**: Este arquivo.
- **requirements.txt**: Lista de dependências Python.
- **.env**: Arquivo contendo as chaves de API necessárias.

## 🛠️ Como Executar a Aplicação
#### Executando a Aplicação Principal

Certifique-se de que todas as dependências estão instaladas conforme a seção de instalação.

Execute o seguinte comando no terminal:

```bash
streamlit run app.py
```

A aplicação será iniciada e você poderá acessá-la através do navegador no endereço fornecido pelo Streamlit (geralmente [http://localhost:8501](http://localhost:8501)).

#### Executando o Conversor de Coordenadas
```bash
streamlit run gmaps.py
```
A aplicação estará disponível no navegador, permitindo a conversão de coordenadas em logradouro e bairro.

### 🧪 Executando os Testes Unitários

Para rodar os testes unitários e validar as funcionalidades da aplicação principal, execute:

```bash
python test_app.py
```

### 🧠 Funcionalidades da IA

Com a integração da API Maritaca AI, você pode obter respostas automatizadas para perguntas pré-definidas sobre os dados carregados. A aplicação fornece uma lista de perguntas selecionáveis, e ao escolher uma delas, a IA gera uma resposta baseada no contexto dos dados.

#### Como Funciona

1. **Seleção de Pergunta**: O usuário seleciona uma pergunta específica a partir de uma lista na barra lateral.
2. **Geração de Contexto**: A aplicação gera um contexto relevante com base nos dados filtrados e na pergunta selecionada.
3. **Resposta da IA**: O contexto e a pergunta são enviados à API Maritaca AI, que processa e retorna uma resposta que é exibida diretamente na interface.

#### Perguntas Disponíveis

- “Quantos óbitos ocorreram em 2021?”
- “Qual a faixa etária mais afetada por acidentes?”
- “Em qual bairro ocorreram mais óbitos?”
- “Qual o tipo de via com mais óbitos?”
- “Quantos óbitos ocorreram em cada dia da semana?”
- “Qual o horário com mais óbitos?”
- “Qual o sexo com mais acidentes?”
- “Qual o mês com mais acidentes?”
- “Qual o dia do mês com mais acidentes?”
- “Qual o período do dia com mais óbitos?”
- “Qual o meio de locomoção com mais óbitos?”
- “Quais os tipos de acidentes mais comuns?”
- “Qual a distribuição de óbitos por tipo de vítima (condutor, passageiro, pedestre) em [ano]?”

> **Nota**: Por enquanto, não é possível inserir perguntas personalizadas. As perguntas devem ser selecionadas a partir da lista disponível.

## 📊 Fonte dos Dados

Os dados utilizados nesta análise foram obtidos a partir do [Infosiga SP](https://www.infosiga.sp.gov.br/?name=identificacao4&contextId=8a80809939587c0901395881fc2b0004).

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests para melhorar este projeto.

## 📝 Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 📬 Contato

- **Autor**: Gabriel Melo
- **Email**: contato@gabrielmelo.com
- **LinkedIn**: [linkedin.com/in/gabriellmelo](http://linkedin.com/in/gabriellmelo/)

---
> **Nota**: Certifique-se de que todas as dependências estão instaladas e as chaves de API estão corretamente configuradas para evitar erros durante a execução.

Atualização: 18/11/2024

--- 


Desenvolvido com ❤️ por Gabriel Melo (https://github.com/gabriellmelo)
