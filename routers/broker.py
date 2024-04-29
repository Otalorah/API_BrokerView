from fastapi import Depends, APIRouter, status

from typing import Annotated

from lib.functions_sheet_broker import get_data_sheet
from lib.functions_jwt import aut_token

router = APIRouter()

# - - - - - - - - - - - - - - - - - - - - - - - - - ENDPOINTS - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# get data from fund sheet


@router.get("/", response_model=list, status_code=status.HTTP_200_OK)
async def get_data_broker(token: Annotated[None, Depends(aut_token)]) -> list[dict]:

    user_sheet = token['user_sheet']

    return get_data_sheet(sheet_name=user_sheet)
