# Análise de Óbitos em Franca/SP

![Escudo de Franca](images/escudo.png)

## Visão Geral

Este projeto consiste em uma aplicação interativa desenvolvida com **Streamlit** para analisar dados de óbitos em acidentes de trânsito na cidade de **Franca**, São Paulo. Através de visualizações dinâmicas e filtros intuitivos, os usuários podem explorar diversas métricas relacionadas aos acidentes, como quantidade de sinistros por ano, distribuição por dia da semana, tipo de veículo envolvido, faixa etária das vítimas, entre outros.

Além disso, o projeto agora conta com a integração da **API Mariaca AI**, permitindo que os usuários façam perguntas diretamente sobre os dados analisados e recebam respostas automatizadas baseadas no contexto dos dados carregados.

## 📊 Funcionalidades

- **Dashboard Interativo**: Visualizações gráficas interativas utilizando **Plotly Express**.
- **Filtros Dinâmicos**: Filtragem de dados por ano para uma análise mais focada.
- **Diversas Métricas**:
  - Quantidade de sinistros por ano.
  - Quantidade de vítimas fatais por ano.
  - Distribuição de sinistros por dia da semana.
  - Distribuição por tipo de veículo.
  - Comparação de gênero x horário do sinistro.
  - Turno com maior incidência de sinistros.
  - Distribuição de óbitos por faixa etária.
  - Óbitos por tipo de via.
  - Óbitos por período do dia.
  - Óbitos por sexo.
  - Óbitos por mês do ano.
  - Óbitos por dia do mês.
- **Formulário de Contato**: Permite aos usuários enviar dúvidas ou comentários diretamente através da aplicação.
- **Assistente de IA**: Integração com a **API Mariaca AI** para responder perguntas baseadas nos dados carregados.

## 🚀 Tecnologias Utilizadas

- **Python 3.8+**
- **Streamlit**: Para construção da interface web interativa.
- **Pandas**: Manipulação e análise de dados.
- **Plotly Express**: Criação de visualizações gráficas.
- **OpenPyXL**: Leitura de arquivos Excel.
- **Mariaca AI**: Integração de IA para responder perguntas automatizadas sobre o dataset.

## 📥 Instalação

### 1. Clone o Repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
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
pip install streamlit pandas plotly openpyxl python-dotenv maritalk
```

### 4. Configuração da API Mariaca

Crie um arquivo `.env` na raiz do projeto e adicione a sua chave da API Mariaca AI:

```bash
MARITACA_API_KEY='sua_chave_api_maritaca'
```

## 🗂️ Estrutura do Projeto

```
seu-repositorio/
├── images/
│   └── escudo.png
├── filtro-franca.xlsx
├── app.py
├── README.md
├── .env
└── requirements.txt
```

- **images/**: Diretório contendo imagens utilizadas na aplicação.
- **filtro-franca.xlsx**: Arquivo Excel com os dados de óbitos em Franca.
- **app.py**: Código fonte da aplicação Streamlit.
- **README.md**: Este arquivo.
- **requirements.txt**: Lista de dependências Python.
- **.env**: Arquivo contendo a chave de API da Mariaca AI.

## 🛠️ Como Executar a Aplicação

Certifique-se de que todas as dependências estão instaladas conforme a seção de instalação.

Execute o seguinte comando no terminal:

```bash
streamlit run app.py
```

A aplicação será iniciada e você poderá acessá-la através do navegador no endereço fornecido pelo Streamlit (geralmente [http://localhost:8501](http://localhost:8501)).

## 🧠 Funcionalidades da IA

Com a integração da API Mariaca AI, você pode fazer perguntas sobre os dados carregados e receber respostas automáticas baseadas no contexto dos dados. A IA utiliza uma abordagem de contextualização dinâmica, onde a aplicação:

1. **Detecta o tipo de pergunta** (por exemplo, se é sobre "ano", "faixa etária" ou "dia da semana").
2. **Gera um contexto relevante** com base nos dados filtrados, que é então enviado à API.
3. **Recebe a resposta da IA** e a exibe diretamente na interface.

### Exemplos de Perguntas

- "Quantos óbitos ocorreram em 2020?"
- "Qual foi o dia da semana com mais acidentes?"
- "Quantos óbitos ocorreram por faixa etária?"

## 📊 Fonte dos Dados

Os dados utilizados nesta análise foram obtidos a partir do [Infosiga SP](https://www.infosiga.sp.gov.br/?name=identificacao4&contextId=8a80809939587c0901395881fc2b0004).

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests para melhorar este projeto.

## 📝 Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 📬 Contato

Para dúvidas ou sugestões, utilize o formulário de contato disponível na aplicação ou entre em contato através do email fornecido.

---

Desenvolvido com ❤️ por Gabriel Melo (https://github.com/gabriellmelo)
