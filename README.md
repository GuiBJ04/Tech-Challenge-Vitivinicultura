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

# Arquitetura

O projeto é estruturado da seguinte forma:

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

