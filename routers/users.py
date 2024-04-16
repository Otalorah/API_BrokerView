from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from typing import Annotated

from models import models

from lib.functions_text import transform_to_bool
from lib.functions_jwt import create_token, aut_user
from lib.functions_sheets import create_user_sheet, get_data_user_sheet, verify_password

router = APIRouter()

# - - - - - - - - - - - - - - - - - - - - - - - - - ENDPOINTS - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Create User in database


@router.post("/create",response_model=dict, status_code=status.HTTP_201_CREATED)
def create_user(user: models.UserCreate):

    username, has_broker, has_fondo = create_user_sheet(user)

    token = create_token(
        username=username, has_broker=has_broker, has_fondo=has_fondo)

    return {"redirect": "/inicio", "access_token": token}

# Login the user with database


@router.post("/login", status_code=status.HTTP_200_OK)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):

    def exception(str): return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail=str)

    db_user = get_data_user_sheet(username=form_data.username)

    if not db_user:
        raise exception("El usuario no existe")

    if not verify_password(form_data.username, form_data.password):
        raise exception("La contraseña no es correcta")

    has_broker, has_fondo = transform_to_bool(db_user[5]), transform_to_bool(db_user[6])

    token = create_token(username=form_data.username,
                         has_broker=has_broker, has_fondo=has_fondo)

    return {"redirect": "/inicio", "access_token": token}

# Get the User with a token


@router.get("/")
def get_user(username: Annotated[None, Depends(aut_user)]):

    # db_user = crud.get_user(db, username=username)

    return username
