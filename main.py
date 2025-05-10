from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from jose import jwt, JWTError
from scrape import get_title, get_content
from security import get_current_user
from config import SECRET_KEY, ALGORITHM
from database import users

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
def get_data_production(
     ano: int = Query(
        default=1970,
        description="Ano da produção vitivinícola (entre 1970 e 2023)",
        ge=1970,
        le=2023),
    username: str = Depends(get_current_user)):
    try:
        url = f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_02'
        scraper = Scraper(url)
        table = scraper.get_table()
        headers = scraper.get_headers()
        paragraphs = scraper.get_paragraphs()

        return {
            "url": url,
            "titulos": headers,
            "paragrafos": paragraphs,
            "dados": table
        }
    except Exception as e:
        return f"Error: {e}"
    
@app.get("/dados-processamento")
def get_data_processing(
     ano: int = Query(
        default=1970,
        description="Ano da processamento das uvas (entre 1970 e 2023)",
        ge=1970,
        le=2023),
    option: int = Query(
        default=1,
        description="1: Viniferas, 2: Americanas e híbridas, 3: Uvas de mesa, 4: Sem classificação",
        ge=1,
        le=4),
    username: str = Depends(get_current_user)):
    
    try:
        urls = [
            f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_03&subopcao=subopt_01',
            f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_03&subopcao=subopt_02',
            f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_03&subopcao=subopt_03',
            f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_03&subopcao=subopt_04'
        ]

        resultados = []

        scraper = Scraper(urls[option-1])
        table = scraper.get_table()
        headers = scraper.get_headers()
        paragraphs = scraper.get_paragraphs()

        resultados.append({
            "url": urls[option-1],
            "categoria": get_category_name(urls[option-1]),
            "titulos": headers,
            "paragrafos": paragraphs,
            "dados": table
        })

        return resultados
    except Exception as e:
        return f"Error: {e}"
    
@app.get("/dados-comercializacao")
def get_data_commercialization(
     ano: int = Query(
        default=1970,
        description="Ano de comercialização dos vinhos (entre 1970 e 2023)",
        ge=1970,
        le=2023),
    username: str = Depends(get_current_user)):
    try:
        url = f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_04'

        scraper = Scraper(url)
        table = scraper.get_table()
        headers = scraper.get_headers()
        paragraphs = scraper.get_paragraphs()

        return {
            "url": url,
            "titulos": headers,
            "paragrafos": paragraphs,
            "dados": table
        }
    except Exception as e:
        return f"Error: {e}"
    
@app.get("/dados-importacao")
def get_data_production(
     ano: int = Query(
        default=1970,
        description="Ano de importação dos vinhos (entre 1970 e 2024)",
        ge=1970,
        le=2024),
    option: int = Query(
        default=1,
        description="1: Vinhos de mesa, 2: Espumantes, 3: Uvas frescas, 4: Uvas passas, 5: Suco de uva",
        ge=1,
        le=5),
    username: str = Depends(get_current_user)):
    try:
        urls = [
            f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_05&subopcao=subopt_01',
            f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_05&subopcao=subopt_02',
            f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_05&subopcao=subopt_03',
            f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_05&subopcao=subopt_04',
            f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_05&subopcao=subopt_05'
        ]

        resultados = []
        scraper = Scraper(urls[option-1])
        table = scraper.get_table()
        headers = scraper.get_headers()
        paragraphs = scraper.get_paragraphs()

        resultados.append({
            "url": urls[option-1],
            "categoria": get_category_name(urls[option-1]),
            "titulos": headers,
            "paragrafos": paragraphs,
            "dados": table
        })

        return resultados
    except Exception as e:
        return f"Error: {e}"
    
@app.get("/dados-exportacao")
def get_data_export(
     ano: int = Query(
        default=1970,
        description="Ano de exportação dos vinhos (entre 1970 e 2024)",
        ge=1970,
        le=2024),
    option: int = Query(
        default=1,
        description="1: Vinhos de mesa, 2: Espumantes, 3: Uvas frescas, 4: Suco de uva",
        ge=1,
        le=4),
    username: str = Depends(get_current_user)):
    try:
        urls = [
            f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_06&subopcao=subopt_01',
            f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_06&subopcao=subopt_02',
            f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_06&subopcao=subopt_03',
            f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_06&subopcao=subopt_04'
        ]

        resultados = []
        scraper = Scraper(urls[option-1])
        table = scraper.get_table()
        headers = scraper.get_headers()
        paragraphs = scraper.get_paragraphs()

        resultados.append({
            "url": urls[option-1],
            "categoria": get_category_name(urls[option-1]),
            "titulos": headers,
            "paragrafos": paragraphs,
            "dados": table
        })

        return resultados
    except Exception as e:
        return f"Error: {e}"