from fastapi import APIRouter, status

from models import models

from lib.functions_smtp import send_email
from lib.functions_users import verify_email, verify_code, write_code_gmail
from lib.utils import generate_code


router = APIRouter()

# - - - - - - - - - - - - - - - - - - - - - - - - - ENDPOINTS - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Verify email user


@router.post("/", response_model=dict, status_code=status.HTTP_200_OK)
async def emails(email: models.EmailUser) -> dict:

    email = dict(email)["email"]

    verify_email(email)

    code = generate_code()

    send_email(email=email, code=code)
    write_code_gmail(email=email, code=code)

    return {"redirect": "/inicio"}


# Verify code user


@router.post("/code", response_model=dict, status_code=status.HTTP_200_OK)
async def codes(user: models.CodeUser) -> dict:

    user = dict(user)
    verify_code(email=user["email"], code=user["code"])

    return {"redirect": "/inicio"}
