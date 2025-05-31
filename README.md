# API de Coleta de Dados Vitivinícolas (Embrapa)

Este projeto realiza o scraping de dados vitivinícolas diretamente do portal da Embrapa Uva e Vinho, armazenando as informações em um banco de dados (SQLite). Além disso, disponibiliza uma API para consulta aos dados coletados, com autenticação via JWT.

## Sumário

- [Arquitetura](#arquitetura)
- [Instalação](#instalação)
- [Como Executar](#como-executar)
- [Endpoints](#endpoints)
  - [Raiz (`/`)](#raiz-)
  - [Login (`/login`)](#login-)
  - [Predict (`/predict`)](#predict-)
  - [List Predictions (`/predictions`)](#list-predictions-)
- [Autenticação](#autenticação)
- [Exemplo de Uso](#exemplo-de-uso)

## Arquitetura

O projeto é estruturado da seguinte forma:

```

TECH-CHALLENGE-VITIVINICULTURA/
├── api/
│   ├── auth/
│   │   ├── pycache/
│   │   ├── auth.py
│   │   └── scraped_data.py
├── db/
│   ├── init.py
│   ├── database.py
│   └── init_db.py
├── models/
│   ├── init.py
│   ├── scraped_data.py
│   └── user.py
├── repository/
│   ├── pycache/
│   └── scraped_data.py
├── security/
│   ├── pycache/
│   ├── config.py
│   └── security.py
├── services/
│   ├── pycache/
│   └── scrape.py
├── utils/
│   ├── pycache/
│   └── helpers.py
├── .gitignore
├── main.py
├── README.md
├── requirements.txt
├── scrape_cache.db
└── user_cache.db

```

A aplicação utiliza:

* **FastAPI** para criação de endpoints.

* **SQLite** com **SQLAlchemy** para persistência.

* **JWT** para autenticação.

* **BeautifulSoup** + **Requests** para web scraping.


## Instalação

1. **Clonar o repositório** (ou copiar o arquivo `app.py` e demais arquivos necessários).

2. **Criar e ativar um ambiente virtual (opcional, mas recomendado)**:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Em sistemas Unix
   venv\Scripts\activate # Em sistemas Windows
   ```
3. **Instalar as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

## Como Executar

1. Inicialize o banco de dados:

```
python db/init_db.py
```

2. Execute o servidor FastAPI:
```
uvicorn main:app --reload
```

A aplicação Flask iniciará em modo debug, por padrão em `http://127.0.0.1:5000/`.

3. Acesse a documentação interativa da API: `htt/p://127.0.0.1:8000/docs`.

## Endpoints

### /login
* Método: POST
* Acesso: Público
* Descrição: Retorna um token JWT válido com credenciais de teste.

### /dados-producao
* Método: GET
* Acesso: Protegido (JWT)
* Descrição: Coleta e retorna os dados de produção vitivinícola do site da Embrapa para um determinado ano.
* Query Parameters:
    **ano: Ano da produção (1970–2023)
* Resposta:
 ```json
 {
  "url": "...",
  "titulos": [...],
  "paragrafos": [...],
  "dados": [...]
} 
```


