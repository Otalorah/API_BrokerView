from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from typing import Annotated

from sqlalchemy.orm import Session
from db import crud, schemas
from db.database import engine, Base

from lib.functions_jwt import create_token, aut_user
from lib.functions_db import get_db


Base.metadata.create_all(bind=engine)

router = APIRouter()

# - - - - - - - - - - - - - - - - - - - - - - - -  - ENDPOINTS - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Create User in database


@router.post("/create", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Annotated[Session, Depends(get_db)]) -> dict:

    db_user = crud.get_user(db, username=user.username)

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="The user exist")

    crud.create_user(db, user)

    token = create_token(user.username)

    return {"redirect": "/inicio", "token": token}

# Login the user with database


@router.post("/login", response_model=dict, status_code=status.HTTP_200_OK)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[Session, Depends(get_db)]) -> dict:

    def exception(str): return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail=str)

    db_user = crud.get_user(db, username=form_data.username)

    if not db_user:
        raise exception("The user doesn't exist")

    if not crud.verify_password(db, form_data.username, form_data.password):
        raise exception("The password isn't correct")

    token = create_token(form_data.username)

    return {"redirect": "/inicio", "token": token}

# Get the User with a token


@router.get("/", response_model=schemas.User)
def get_user(username: Annotated[None, Depends(aut_user)], db: Session = Depends(get_db)) -> schemas.UserBase:

    db_user = crud.get_user(db, username=username)

    return db_user
