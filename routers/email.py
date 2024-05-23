from fastapi import APIRouter, status

from models import models

from lib.functions_smtp import send_email
from lib.functions_users import verify_email, verify_code
from lib.utils import generate_code


router = APIRouter()

# - - - - - - - - - - - - - - - - - - - - - - - - - ENDPOINTS - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Verify email user


@router.post("/", response_model=dict, status_code=status.HTTP_200_OK)
async def emails(email: models.EmailUser) -> dict:

    email = dict(email)["email"]

    verify_email(email)

    code_str = generate_code()
    send_email(to_email=email, code=code_str)

    return {"message": "Correo enviado correctamente"}


# Verify code user


@router.post("/code", response_model=dict, status_code=status.HTTP_200_OK)
async def codes(user: models.CodeUser) -> dict:

    user = dict(user)
    verify_code(email=user["email"], code=user["code"])

    return {"redirect": "/inicio"}
