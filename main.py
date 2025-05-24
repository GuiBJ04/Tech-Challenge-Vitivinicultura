from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from jose import jwt, JWTError
from security import get_current_user
from config import SECRET_KEY, ALGORITHM
from scrape import Scraper
from helpers import get_category_name
from database import Session, SessionLocal
from models.scraped_data import ScrapedData
from models.user import UserData
from utils.cache import salvar_scraping
import json
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

app = FastAPI(
    title="API Vitivinicultura", 
    description="API pública baseada em dados da Embrapa.",
    version="1.0"
)

# Autenticação
security_basic = HTTPBasic()

@app.post("/register")
def registro(username: str, password: str):
    db = Session()

    user_exists = db.query(UserData).filter_by(user=username).first()
    if user_exists:
        db.close()
        raise HTTPException(status_code=400, detail="Usuário já existe")

    new_user = UserData(user=username, password=password)
    db.add(new_user)
    db.commit()
    db.close()

    return {"message": "Usuário criado com sucesso"}

# Endpoint de login com HTTP Basic
@app.get("/login")
def login(credentials: HTTPBasicCredentials = Depends(security_basic)):
    db = Session()
    user = db.query(UserData).filter_by(user=credentials.username).first()

    if not user or user.password != credentials.password:
        db.close()
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    sao_paulo_tz = ZoneInfo("America/Sao_Paulo")
    now = datetime.now(sao_paulo_tz)
    expiration = now + timedelta(hours=1)

    payload = {
        "sub": credentials.username,
        "iat": int(now.timestamp()),
        "exp": int(expiration.timestamp())
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    db.close()

    return {
        "access_token": token,
        "token_type": "bearer",
        "expired_at": expiration.isoformat()
    }

@app.get(
    "/dados-producao",
    summary="Consulta dados de produção",
    description="Retorna dados de produção de produtos da vitivinicultura com base na Embrapa. "
                "É possível filtrar os dados por ano (1970 a 2023). Se o site estiver offline, dados são retornados do cache local."
)
def get_data_production(
    username: str = Depends(get_current_user),
    ano: int = Query(
        default=1970,
        description="Ano da produção vitivinícola (entre 1970 e 2023)",
        ge=1970,
        le=2023
    )
):
    try:
        base_url = 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02'

        if ano:
            url = f"{base_url}&ano={ano}"
        else:
            url = base_url

        db = SessionLocal()

        scraper = Scraper(url)
        table = scraper.get_table()
        headers = scraper.get_headers()
        paragraphs = scraper.get_paragraphs()

        salvar_scraping(db, url, "produção", headers, paragraphs, table, ano)

        return {
            "url": url,
            "ano": ano,
            "titulos": headers,
            "paragrafos": paragraphs,
            "dados": table
        }
    except Exception:
        cache = db.query(ScrapedData).filter_by(url=url, ano=ano).first()

        if cache:
            return {
                "fonte": "cache",
                "url": url,
                "ano": ano,
                "titulos": json.loads(cache.titulos),
                "paragrafos": json.loads(cache.paragrafos),
                "dados": json.loads(cache.dados_json)
            }
        else:
            raise HTTPException(status_code=503, detail="Fonte indisponível e sem cache local.")

@app.get(
    "/dados-processamento",
    summary="Consulta dados de processamento",
    description="Retorna dados de processamento de produtos da vitivinicultura com base na Embrapa. "
                "É possível filtrar os dados por ano (1970 a 2023). Se o site estiver offline, dados são retornados do cache local."
)
@app.get("/dados-processamento")
def get_data_processing(
    username: str = Depends(get_current_user),
        ano: int = Query(
        default=1970,
        description="Ano da processamento das uvas (entre 1970 e 2023)",
        ge=1970,
        le=2023),
    option: int = Query(
        default=1,
        description="1: Viniferas, 2: Americanas e híbridas, 3: Uvas de mesa, 4: Sem classificação",
        ge=1,
        le=4)
):
    urls = [
            f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_03&subopcao=subopt_01',
            f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_03&subopcao=subopt_02',
            f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_03&subopcao=subopt_03',
            f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_03&subopcao=subopt_04'
        ]

    db = SessionLocal()
    resultados = []    

    try:
        scraper = Scraper(urls[option-1])
        table = scraper.get_table()
        headers = scraper.get_headers()
        paragraphs = scraper.get_paragraphs()
        categoria = get_category_name(urls[option-1])

        salvar_scraping(db, urls[option-1], categoria, headers, paragraphs, table, ano)

        resultados.append({
            "fonte": "web",
            "url": urls[option-1],
            "ano": ano,
            "categoria": categoria,
            "titulos": headers,
            "paragrafos": paragraphs,
            "dados": table
        })
    except Exception:
        cache = db.query(ScrapedData).filter_by(url=urls[option-1], ano=ano).first()
        if cache:
            resultados.append({
                "fonte": "cache",
                "url": urls[option-1],
                "ano": ano,
                "categoria": cache.categoria,
                "titulos": json.loads(cache.titulos),
                "paragrafos": json.loads(cache.paragrafos),
                "dados": json.loads(cache.dados_json)
            })

    if not resultados:
        raise HTTPException(status_code=503, detail="Nenhuma fonte disponível ou cache encontrado.")
    return resultados

@app.get(
    "/dados-comercializacao",
    summary="Consulta dados de comercializacao",
    description="Retorna dados de comercializacao de produtos da vitivinicultura com base na Embrapa. "
                "É possível filtrar os dados por ano (1970 a 2023). Se o site estiver offline, dados são retornados do cache local."
)
def get_data_commercialization(
    username: str = Depends(get_current_user),
        ano: int = Query(
        default=1970,
        description="Ano da produção vitivinícola (entre 1970 e 2023)",
        ge=1970,
        le=2023
    )
):
    base_url = 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_04'

    if ano:
        url = f"{base_url}&ano={ano}"
    else:
        url = base_url

    db = SessionLocal()

    try:
        scraper = Scraper(url)
        table = scraper.get_table()
        headers = scraper.get_headers()
        paragraphs = scraper.get_paragraphs()

        salvar_scraping(db, url, "comercializacao", headers, paragraphs, table, ano)

        return {
            "fonte": "web",
            "url": url,
            "ano": ano,
            "categoria": "comercializacao",
            "titulos": headers,
            "paragrafos": paragraphs,
            "dados": table
        }

    except Exception:
        cache = db.query(ScrapedData).filter_by(url=url, ano=ano).first()
        if cache:
            return {
                "fonte": "cache",
                "url": url,
                "ano": ano,
                "categoria": cache.categoria,
                "titulos": json.loads(cache.titulos),
                "paragrafos": json.loads(cache.paragrafos),
                "dados": json.loads(cache.dados_json)
            }
        raise HTTPException(status_code=503, detail="Fonte indisponível e sem cache local.")

@app.get(
    "/dados-importacao",
    summary="Consulta dados de importação",
    description="Retorna dados de importação de produtos da vitivinicultura com base na Embrapa. "
                "É possível filtrar os dados por ano (1970 a 2024). Se o site estiver offline, dados são retornados do cache local."
)
def get_data_import(
    username: str = Depends(get_current_user),
        ano: int = Query(
        default=1970,
        description="Ano de importação dos vinhos (entre 1970 e 2024)",
        ge=1970,
        le=2024),
    option: int = Query(
        default=1,
        description="1: Vinhos de mesa, 2: Espumantes, 3: Uvas frescas, 4: Uvas passas, 5: Suco de uva",
        ge=1,
        le=5)
):
    urls = [
            f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_05&subopcao=subopt_01',
            f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_05&subopcao=subopt_02',
            f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_05&subopcao=subopt_03',
            f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_05&subopcao=subopt_04',
            f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_05&subopcao=subopt_05'
        ]

    db = SessionLocal()
    resultados = []

    try:
        scraper = Scraper(urls[option-1])
        table = scraper.get_table()
        headers = scraper.get_headers()
        paragraphs = scraper.get_paragraphs()
        categoria = get_category_name(urls[option-1])

        salvar_scraping(db, urls[option-1], categoria, headers, paragraphs, table, ano)

        resultados.append({
            "fonte": "web",
            "url": urls[option-1],
            "ano": ano,
            "categoria": categoria,
            "titulos": headers,
            "paragrafos": paragraphs,
            "dados": table
        })

    except Exception:
        cache = db.query(ScrapedData).filter_by(url=urls[option-1], ano=ano).first()
        if cache:
            resultados.append({
                "fonte": "cache",
                "url": urls[option-1],
                "ano": ano,
                "categoria": cache.categoria,
                "titulos": json.loads(cache.titulos),
                "paragrafos": json.loads(cache.paragrafos),
                "dados": json.loads(cache.dados_json)
            })

    if not resultados:
        raise HTTPException(status_code=503, detail="Nenhuma fonte disponível ou cache encontrado.")
    return resultados
    
@app.get(
    "/dados-exportacao",
    summary="Consulta dados de importação",
    description="Retorna dados de exportação de produtos da vitivinicultura com base na Embrapa. "
                "É possível filtrar os dados por ano (1970 a 2024). Se o site estiver offline, dados são retornados do cache local."
)
@app.get("/dados-exportacao")
def get_data_export(
    username: str = Depends(get_current_user),
        ano: int = Query(
        default=1970,
        description="Ano de exportação dos vinhos (entre 1970 e 2024)",
        ge=1970,
        le=2024),
    option: int = Query(
        default=1,
        description="1: Vinhos de mesa, 2: Espumantes, 3: Uvas frescas, 4: Suco de uva",
        ge=1,
        le=4)
):
    urls = [
            f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_06&subopcao=subopt_01',
            f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_06&subopcao=subopt_02',
            f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_06&subopcao=subopt_03',
            f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_06&subopcao=subopt_04'
        ]

    db = SessionLocal()
    resultados = []


    try:
        scraper = Scraper(urls[option-1])
        table = scraper.get_table()
        headers = scraper.get_headers()
        paragraphs = scraper.get_paragraphs()
        categoria = get_category_name(urls[option-1])

        salvar_scraping(db, urls[option-1], categoria, headers, paragraphs, table, ano)

        resultados.append({
            "fonte": "web",
            "url": urls[option-1],
            "ano": ano,
            "categoria": categoria,
            "titulos": headers,
            "paragrafos": paragraphs,
            "dados": table
        })

    except Exception:
        cache = db.query(ScrapedData).filter_by(url=urls[option-1], ano=ano).first()
        if cache:
            resultados.append({
                "fonte": "cache",
                "url": urls[option-1],
                "ano": ano,
                "categoria": cache.categoria,
                "titulos": json.loads(cache.titulos),
                "paragrafos": json.loads(cache.paragrafos),
                "dados": json.loads(cache.dados_json)
            })

    if not resultados:
        raise HTTPException(status_code=503, detail="Nenhuma fonte disponível ou cache encontrado.")
    return resultados