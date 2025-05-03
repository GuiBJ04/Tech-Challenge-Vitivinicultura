from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from jose import jwt, JWTError
from security import get_current_user
from config import SECRET_KEY, ALGORITHM
from database import users
from scrape import Scraper
from helpers import get_category_name

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

@app.get("/")
def hello():
    return "Hello Fast"

@app.get("/dados-producao")
def get_data_production(username: str = Depends(get_current_user)):
    try:
        url = 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02'
        scraper = Scraper(url)
        table = scraper.get_table()
        return scraper.get_table()
    except Exception as e:
        return f"Error: {e}"
    
@app.get("/dados-processamento")
def get_data_processing(username: str = Depends(get_current_user)):
    try:
        urls = [
            'http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_01&opcao=opt_03',
            'http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_02&opcao=opt_03',
            'http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_03&opcao=opt_03',
            'http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_04&opcao=opt_03',
        ]

        resultados = []
        for url in urls:
            scraper = Scraper(url)
            table = scraper.get_table()

            nome_categoria = get_category_name(url)
            if nome_categoria != '':
                resultados.append({
                    "url": url,
                    "categoria": nome_categoria,
                    "dados": table
                })
            else:
                 resultados.append({
                    "url": url,
                    "dados": table
                })

        return resultados
    except Exception as e:
        return f"Error: {e}"
    
@app.get("/dados-comercializacao")
def get_data_commercialization(username: str = Depends(get_current_user)):
    try:
        url = 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_04'

        scraper = Scraper(url)
        table = scraper.get_table()

        return {
            "url": url,
            "dados": table
        }
    except Exception as e:
        return f"Error: {e}"
    
@app.get("/dados-importacao")
def get_data_production(username: str = Depends(get_current_user)):
    try:
        urls = [
            'http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_01&opcao=opt_05',
            'http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_02&opcao=opt_05',
            'http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_03&opcao=opt_05',
            'http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_04&opcao=opt_05',
            'http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_05&opcao=opt_05',
        ]

        resultados = []
        for url in urls:
            scraper = Scraper(url)
            table = scraper.get_table()

            nome_categoria = get_category_name(url)
            if nome_categoria != '':
                resultados.append({
                    "url": url,
                    "categoria": nome_categoria,
                    "dados": table
                })
            else:
                 resultados.append({
                    "url": url,
                    "dados": table
                })

        return resultados
    except Exception as e:
        return f"Error: {e}"
    
@app.get("/dados-exportacao")
def get_data_export(username: str = Depends(get_current_user)):
    try:
        urls = [
            'http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_01&opcao=opt_06',
            'http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_02&opcao=opt_06',
            'http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_03&opcao=opt_06',
            'http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_04&opcao=opt_06',
        ]

        resultados = []
        for url in urls:
            scraper = Scraper(url)
            table = scraper.get_table()
            headers = scraper.get_headers()
            paragraphs = scraper.get_paragraphs()

            resultados.append({
                "url": url,
                "categoria": get_category_name(url),
                "titulos": headers,
                "paragrafos": paragraphs,
                "dados": table
            })

        return resultados
    except Exception as e:
        return f"Error: {e}"