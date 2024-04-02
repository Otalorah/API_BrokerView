from jose import jwt, JWTError

from os import getenv
from dotenv import load_dotenv

from datetime import datetime, timedelta, UTC

load_dotenv()

SECRET = getenv("SECRET")
ALGORITHM = getenv("ALGORITHM")
ACCESS_TOKEN_DURATION = 1


def Write_token(username: str):
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_DURATION)
    access_token = {"sub": username, "exp": expire}
    return jwt.encode(access_token, SECRET, algorithm=ALGORITHM)


def Verify_token(token: str, output: bool = False) -> str | bool:
    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")

    except JWTError:
        return False

    if output:
        return username
    return True
