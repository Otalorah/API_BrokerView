from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from typing import Annotated

from models import models

from lib.functions_jwt import create_token, aut_user
from lib.functions_sheets import create_user_sheet

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
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> dict:

    def exception(str): return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail=str)

    # db_user = crud.get_user(db, username=form_data.username)

    # if not db_user:
    #     raise exception("The user doesn't exist")

    # if not crud.verify_password(db, form_data.username, form_data.password):
    #     raise exception("The password isn't correct")

    # token = create_token(form_data.username)

    return form_data

# Get the User with a token


@router.get("/", response_model=models.User)
def get_user(username: Annotated[None, Depends(aut_user)]) -> models.UserBase:

    # db_user = crud.get_user(db, username=username)

    return username
