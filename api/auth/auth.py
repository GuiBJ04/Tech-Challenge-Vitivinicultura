from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from jose import jwt
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta
from pydantic import BaseModel

from db.database import Session
from models.user import UserData
from security.config import SECRET_KEY, ALGORITHM

router = APIRouter()

security_basic = HTTPBasic()

class RegisterInput(BaseModel):
    username: str
    password: str


@router.post("/register")
def registro(payload: RegisterInput):

    username = payload.username
    password = payload.password

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

@router.get("/login")
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
