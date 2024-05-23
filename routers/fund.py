from fastapi import Depends, APIRouter, status

from typing import Annotated

from lib.functions_fund import get_data_sheet, convert_to_dictionary
from lib.functions_jwt import aut_token

router = APIRouter()

# - - - - - - - - - - - - - - - - - - - - - - - - - ENDPOINTS - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

#get data from fund sheet


@router.get("/", response_model=list, status_code=status.HTTP_200_OK)
async def get_data_fund(token: Annotated[None, Depends(aut_token)]) -> list[dict]:

    user_sheet = token['user_sheet']
    data_list = get_data_sheet(user_sheet)
    return convert_to_dictionary(data=data_list)
