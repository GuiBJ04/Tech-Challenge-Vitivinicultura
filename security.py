from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from config import SECRET_KEY, ALGORITHM
from database import Session
from models.user import UserData

security_bearer = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security_bearer)):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    db = Session()
    user = db.query(UserData).filter_by(user=username).first()
    db.close()

    if user is None:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    return username