from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from typing import Annotated

from models import models

from lib.utils import transform_to_bool
from lib.functions_jwt import create_token_user, aut_user, aut_token
from lib.functions_users import create_user_sheet, get_data_user, verify_password

router = APIRouter()

# - - - - - - - - - - - - - - - - - - - - - - - - - ENDPOINTS - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Create User in database


@router.post("/create", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_user(user: models.UserCreate) -> dict:

    username, has_broker, has_fund, name_sheet_user = create_user_sheet(user)

    token = create_token_user(
        username=username, has_broker=has_broker, has_fund=has_fund, user_sheet=name_sheet_user)

    return {"redirect": "/password", "access_token": token}

# Login the user with database


@router.post("/login", response_model=dict, status_code=status.HTTP_200_OK)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> dict:

    def exception(str): return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail=str)

    db_user = get_data_user(username=form_data.username)

    if not db_user:
        raise exception("El usuario no existe")

    if not verify_password(form_data.username, form_data.password):
        raise exception("La contraseña no es correcta")

    has_broker, has_fund = transform_to_bool(
        db_user['has_broker']), transform_to_bool(db_user['has_fund'])

    name_user_sheet = db_user['user_sheet']

    token = create_token_user(username=form_data.username,
                              has_broker=has_broker, has_fund=has_fund, user_sheet=name_user_sheet)

    return {"redirect": "/inicio", "access_token": token}

# Get the User with a token


@router.get("/", response_model=models.UserBase, status_code=status.HTTP_200_OK)
def get_user(username: Annotated[None, Depends(aut_user)]) -> models.UserBase:
    return get_data_user(username=username)

# Get the value token with a token


@router.get("/token", response_model=dict, status_code=status.HTTP_200_OK)
def get_token(token: Annotated[None, Depends(aut_token)]) -> dict[str]:
    return token


@router.put("/password")
def change_password(token: Annotated[None, Depends(aut_token)]):
    return token["email"]
