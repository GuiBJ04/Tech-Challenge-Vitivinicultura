# API de Coleta de Dados Vitivinícolas (Embrapa)

Este projeto realiza o scraping de dados vitivinícolas diretamente do portal da Embrapa Uva e Vinho, armazenando as informações em um banco de dados (SQLite). Além disso, disponibiliza uma API para consulta aos dados coletados, com autenticação via JWT.

## Sumário

- [Arquitetura](#arquitetura)
- [Instalação](#instalação)
- [Como Executar](#como-executar)
- [Endpoints](#endpoints)
  - [Registro de usuário (`/register`)](#/register-)
  - [Login (`/login`)](#/ogin-)
  - [Dados de Produção (`/dados-producao`)](#/dados-producao-)
  - [Dados de processamento (`/dados-processamento`)](#/dados-processamento-)
  - [Dados de importação (`/dados-importacao`)](#/dados-importacao-)
  - [Dados de comercialização (`/dados-comercializacao`)](#/dados-comercializacao-)
  - [Dados de Importação (`/dados-importacao`)](#/dados-importacao-)

# Arquitetura

O projeto está estruturado da seguinte forma:

```

TECH-CHALLENGE-VITIVINICULTURA/
├── api/
│   ├── auth/
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
│   └── scraped_data.py
├── security/
│   ├── config.py
│   └── security.py
├── services/
│   └── scrape.py
├── utils/
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

### /register
- Método: POST
- Acesso: Público
- Descrição: Retorna mensagem sob status de criação do usuário. 
- Corpo (JSON):
  ```json
  {
    "username": "username",
    "password": "password"
  }
  ```

Caso seja um novo usuário, retorna:
```json
{
  "message": "Usuário criado com sucesso"
}
```

Caso usuário já exista, retorna:
```json
{
  "detail": "Usuário já existe"
}
```

### /login
- Método: POST
- Acesso: Protegido (HTTPBasic)
- Descrição: Retorna um token JWT válido com credenciais de teste.

```json
{
  "access_token": "token",
  "token_type": "bearer",
  "expired_at": "..."
}
```

### /dados-producao
- Método: GET
- Acesso: Protegido (JWT)
- Descrição: Coleta e retorna os dados de produção vitivinícola do site da Embrapa para um determinado ano.
- Query Parameters:
    - ano: Ano da produção (1970–2023)
- Resposta:
 ```json
 {
  "url": "...",
  "ano": "..."
  "titulos": [...],
  "paragrafos": [...],
  "dados": [...]
} 
```

### /dados-processamento
- Método: GET
- Acesso: Protegido (JWT)
- Descrição: Retorna dados de processamento de produtos da vitivinicultura com base na Embrapa. É possível filtrar os dados por ano (1970 a 2023). Se o site estiver offline, dados são retornados do cache local. 
- Query Parameters:
    - ano: Ano da produção (1970–2023)
- Resposta:
 ```json
 {
  "url": "...",
  "ano": "..."
  "titulos": [...],
  "paragrafos": [...],
  "dados": [...]
} 
```

### /dados-importacao
- Método: GET
- Acesso: Protegido (JWT)
- Descrição: Retorna dados de importação de produtos da vitivinicultura com base na Embrapa. É possível filtrar os dados por ano (1970 a 2024). Se o site estiver offline, dados são retornados do cache local. 
- Query Parameters:
    - ano: Ano da produção (1970–2023)
- Resposta:
 ```json
 {
  "url": "...",
  "ano": "..."
  "titulos": [...],
  "paragrafos": [...],
  "dados": [...]
} 
```

### /dados-comercializacao
- Método: GET
- Acesso: Protegido (JWT)
- Descrição: Retorna dados de comercializacao de produtos da vitivinicultura com base na Embrapa. É possível filtrar os dados por ano (1970 a 2023). Se o site estiver offline, dados são retornados do cache local.
- Query Parameters:
    - ano: Ano da produção (1970–2023)
- Resposta:
 ```json
 {
  "url": "...",
  "ano": "..."
  "titulos": [...],
  "paragrafos": [...],
  "dados": [...]
} 
```

### /dados-importacao
- Método: GET
- Acesso: Protegido (JWT)
- Descrição: Retorna dados de exportação de produtos da vitivinicultura com base na Embrapa. É possível filtrar os dados por ano (1970 a 2024). Se o site estiver offline, dados são retornados do cache local. 
- Query Parameters:
    - ano: Ano da produção (1970–2023)
- Resposta:
 ```json
 {
  "url": "...",
  "ano": "..."
  "titulos": [...],
  "paragrafos": [...],
  "dados": [...]
} 
```
