from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from jose import jwt, JWTError
from security import get_current_user
from config import SECRET_KEY, ALGORITHM
from database import users
from scrape import Scraper
from helpers import get_category_name
from database import SessionLocal
from models.scraped_data import ScrapedData
from utils.cache import salvar_scraping
import json

app = FastAPI()

# Autenticação
security_basic = HTTPBasic()

# Endpoint de login com HTTP Basic
@app.post("/login")
def login(credentials: HTTPBasicCredentials = Depends(security_basic)):
    if credentials.username not in users or users[credentials.username] != credentials.password:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = jwt.encode({"sub": credentials.username}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

@app.get("/dados-producao")
def get_data_production(username: str = Depends(get_current_user)):
    try:
        url = 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02'
        db = SessionLocal()

        scraper = Scraper(url)
        table = scraper.get_table()
        headers = scraper.get_headers()
        paragraphs = scraper.get_paragraphs()

        salvar_scraping(db, url, "produção", headers, paragraphs, table)

        return {
            "url": url,
            "titulos": headers,
            "paragrafos": paragraphs,
            "dados": table
        }
    except Exception:
        cache = db.query(ScrapedData).filter_by(url=url).first()

        if cache:
            return {
                "fonte": "cache",
                "url": url,
                "titulos": json.loads(cache.titulos),
                "paragrafos": json.loads(cache.paragrafos),
                "dados": json.loads(cache.dados_json)
            }
        else:
            raise HTTPException(status_code=503, detail="Fonte indisponível e sem cache local.")

    
@app.get("/dados-processamento")
def get_data_processing(username: str = Depends(get_current_user)):
    urls = [
        'http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_01&opcao=opt_03',
        'http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_02&opcao=opt_03',
        'http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_03&opcao=opt_03',
        'http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_04&opcao=opt_03',
    ]

    db = SessionLocal()
    resultados = []

    for url in urls:
        try:
            scraper = Scraper(url)
            table = scraper.get_table()
            headers = scraper.get_headers()
            paragraphs = scraper.get_paragraphs()
            categoria = get_category_name(url)

            salvar_scraping(db, url, categoria, headers, paragraphs, table)

            resultados.append({
                "fonte": "web",
                "url": url,
                "categoria": categoria,
                "titulos": headers,
                "paragrafos": paragraphs,
                "dados": table
            })
        except Exception:
            cache = db.query(ScrapedData).filter_by(url=url).first()
            if cache:
                resultados.append({
                    "fonte": "cache",
                    "url": url,
                    "categoria": cache.categoria,
                    "titulos": json.loads(cache.titulos),
                    "paragrafos": json.loads(cache.paragrafos),
                    "dados": json.loads(cache.dados_json)
                })

    if not resultados:
        raise HTTPException(status_code=503, detail="Nenhuma fonte disponível ou cache encontrado.")
    return resultados

    
@app.get("/dados-comercializacao")
def get_data_commercialization(username: str = Depends(get_current_user)):
    url = 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_04'
    db = SessionLocal()

    try:
        scraper = Scraper(url)
        table = scraper.get_table()
        headers = scraper.get_headers()
        paragraphs = scraper.get_paragraphs()

        salvar_scraping(db, url, "comercializacao", headers, paragraphs, table)

        return {
            "fonte": "web",
            "url": url,
            "categoria": "comercializacao",
            "titulos": headers,
            "paragrafos": paragraphs,
            "dados": table
        }

    except Exception:
        cache = db.query(ScrapedData).filter_by(url=url).first()
        if cache:
            return {
                "fonte": "cache",
                "url": url,
                "categoria": cache.categoria,
                "titulos": json.loads(cache.titulos),
                "paragrafos": json.loads(cache.paragrafos),
                "dados": json.loads(cache.dados_json)
            }
        raise HTTPException(status_code=503, detail="Fonte indisponível e sem cache local.")
    
@app.get("/dados-importacao")
def get_data_import(username: str = Depends(get_current_user)):
    urls = [
        'http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_01&opcao=opt_05',
        'http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_02&opcao=opt_05',
        'http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_03&opcao=opt_05',
        'http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_04&opcao=opt_05',
        'http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_05&opcao=opt_05',
    ]

    db = SessionLocal()
    resultados = []

    for url in urls:
        try:
            scraper = Scraper(url)
            table = scraper.get_table()
            headers = scraper.get_headers()
            paragraphs = scraper.get_paragraphs()
            categoria = get_category_name(url)

            salvar_scraping(db, url, categoria, headers, paragraphs, table)

            resultados.append({
                "fonte": "web",
                "url": url,
                "categoria": categoria,
                "titulos": headers,
                "paragrafos": paragraphs,
                "dados": table
            })

        except Exception:
            cache = db.query(ScrapedData).filter_by(url=url).first()
            if cache:
                resultados.append({
                    "fonte": "cache",
                    "url": url,
                    "categoria": cache.categoria,
                    "titulos": json.loads(cache.titulos),
                    "paragrafos": json.loads(cache.paragrafos),
                    "dados": json.loads(cache.dados_json)
                })

    if not resultados:
        raise HTTPException(status_code=503, detail="Nenhuma fonte disponível ou cache encontrado.")
    return resultados
    
@app.get("/dados-exportacao")
def get_data_export(username: str = Depends(get_current_user)):
    urls = [
        'http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_01&opcao=opt_06',
        'http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_02&opcao=opt_06',
        'http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_03&opcao=opt_06',
        'http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_04&opcao=opt_06',
    ]

    db = SessionLocal()
    resultados = []

    for url in urls:
        try:
            scraper = Scraper(url)
            table = scraper.get_table()
            headers = scraper.get_headers()
            paragraphs = scraper.get_paragraphs()
            categoria = get_category_name(url)

            salvar_scraping(db, url, categoria, headers, paragraphs, table)

            resultados.append({
                "fonte": "web",
                "url": url,
                "categoria": categoria,
                "titulos": headers,
                "paragrafos": paragraphs,
                "dados": table
            })

        except Exception:
            cache = db.query(ScrapedData).filter_by(url=url).first()
            if cache:
                resultados.append({
                    "fonte": "cache",
                    "url": url,
                    "categoria": cache.categoria,
                    "titulos": json.loads(cache.titulos),
                    "paragrafos": json.loads(cache.paragrafos),
                    "dados": json.loads(cache.dados_json)
                })

    if not resultados:
        raise HTTPException(status_code=503, detail="Nenhuma fonte disponível ou cache encontrado.")
    return resultados