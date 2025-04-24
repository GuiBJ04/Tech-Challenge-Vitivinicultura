from fastapi import FastAPI, Depends, HTTPException
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

@app.get("/")
def hello():
    return "Hello Fast"

@app.get("/site")
def get_site(url: str, username: str = Depends(get_current_user)):
    title = get_title(url)
    headers, paragraphs = get_content(url)
    return {
        "user": username,
        "title": title,
        "headers": headers,
        "paragraphs": paragraphs
    }
