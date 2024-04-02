from fastapi import Depends, APIRouter, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from db import crud, schemas
from db.database import SessionLocal, engine, Base

from passlib.context import CryptContext

from lib.functions_jwt import Write_token, Verify_token

Base.metadata.create_all(bind=engine)

router = APIRouter()

Oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

# Dependencies


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# - - - - - - - - - - - - - - - - - - - - - - - -  - ENDPOINTS - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Create User in database


@router.post("/create", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_user(response: Response, user: schemas.UserCreate, db: Session = Depends(get_db)) -> dict:

    db_user = crud.get_user(db, username=user.username)

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="The user exist")

    crud.create_user(db, user)

    token = Write_token(user.username)

    # Create cookie

    response.set_cookie(key="jwt", value=token, httponly=True)

    return {"message": "User created", "redirect": "/inicio"}

# Login the user with database


@router.post("/login", response_model=dict, status_code=status.HTTP_200_OK)
def login(response: Response, form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> dict:

    def exception(str): return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail=str)

    db_user = crud.get_user(db, username=form.username)

    if not db_user:
        raise exception("The user doesn't exist")

    if not crud.verify_password(db, form.username, form.password):
        raise exception("The password isn't correct")

    token = Write_token(form.username)

    # Create cookie

    response.set_cookie(key="jwt", value=token, httponly=True)

    return {"message": "login succesful"}

# Get the User with a token


@router.get("/", response_model=schemas.UserBase)
def get_user(request: Request, db: Session = Depends(get_db)) -> schemas.UserBase:

    user_validate = Verify_token(request.cookies.get("jwt"), output=True)

    if not user_validate:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    db_user = crud.get_user(db, username=user_validate)

    return db_user
