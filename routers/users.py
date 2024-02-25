from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from db import crud, schemas
from db.database import SessionLocal, engine, Base

from jose import jwt, JWTError
from passlib.context import CryptContext

from datetime import datetime, timedelta

Base.metadata.create_all(bind=engine)

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 3
SECRET = "2109238899c5bb2f4fcf4975ea1c28da09781ebc33ca4ba1e1e4fd000bf76548"

router = APIRouter()

Oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def aut_user(token : str = Depends(Oauth2)):

    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                              detail="No autorizado.", 
                              headers={"WWW-Aunthenticate":"Bearer"})

    try:
        username = jwt.decode(token,SECRET,algorithms=ALGORITHM).get("sub")
    except JWTError:
        raise exception
    if username is None: raise exception

    return username

# - - - - - - - - - - - - - - - - - - - - - - - -  - ENDPOINTS - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

#Create User in database
@router.post("/", response_model = schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, username=user.username)
    
    if db_user: raise HTTPException(status_code=400, detail="The user's exist")
    
    return crud.create_user(db,user)

#Login the user with database
@router.post("/login", response_model = dict)
def login(form : OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    exception = lambda str: HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str)
    
    db_user = crud.get_user(db, username=form.username)
    if not db_user: raise exception("The user doesn't exist")

    if not crud.verify_password(db,form.username,form.password):
            raise exception("The password isn't correct")

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
    access_token = {"sub":form.username,"exp":expire}

    return {"access_token":jwt.encode(access_token,SECRET,algorithm=ALGORITHM),"token_type":"bearer"}

#Get the User with a token
@router.get("/", response_model = schemas.User)
def get_user(user: None | schemas.UserBase = Depends(aut_user), db: Session = Depends(get_db)):
    db_user = crud.get_user(db, username=user)
    return db_user