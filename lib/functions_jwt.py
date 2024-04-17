from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

from pydantic import BaseModel

from jose import jwt, JWTError

from os import getenv
from dotenv import load_dotenv

from datetime import datetime, timedelta, UTC

load_dotenv()

SECRET = getenv("SECRET")
ALGORITHM = getenv("ALGORITHM")
ACCESS_TOKEN_DAYS_DURATION = 1

Oauth2 = OAuth2PasswordBearer(tokenUrl="login")

class Token(BaseModel):
    token: str
    token_type: str = 'bearer'


def create_token(username: str, has_broker: bool, has_fondo: bool) -> Token:
    
    expire = datetime.now(UTC) + timedelta(days=ACCESS_TOKEN_DAYS_DURATION)
    content = {"sub": username, "broker": has_broker,
               "fondo": has_fondo, "exp": expire}
    token = jwt.encode(content, SECRET, algorithm=ALGORITHM)

    return Token(token=token)


async def aut_user(token: str = Depends(Oauth2)) -> str | None:

    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                              detail="No autorizado",
                              headers={"WWW-Aunthenticate": "Bearer"})

    try:
        username = jwt.decode(token, SECRET, algorithms=ALGORITHM).get("sub")
    except JWTError:
        raise exception
    
    if username is None:
        raise exception

    return username

async def aut_token(token: str = Depends(Oauth2)) -> str | None:

    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                              detail="No autorizado",
                              headers={"WWW-Aunthenticate": "Bearer"})

    try:
        token = jwt.decode(token, SECRET, algorithms=ALGORITHM)
    except JWTError:
        raise exception
    
    if token is None:
        raise exception

    return token