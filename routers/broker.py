from fastapi import Depends, APIRouter, status

from typing import Annotated

from lib.functions_sheet_broker import get_data_sheet_broker, convert_to_dictionary
from lib.functions_jwt import aut_token

router = APIRouter()

# - - - - - - - - - - - - - - - - - - - - - - - - - ENDPOINTS - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# get data from fund sheet


@router.get("/", response_model=dict, status_code=status.HTTP_200_OK)
async def get_data_broker(token: Annotated[None, Depends(aut_token)]) -> dict:

    user_sheet = token['user_sheet']

    table1, table2 = get_data_sheet_broker(sheet_name=user_sheet)
    table1 = convert_to_dictionary(data=table1)

    if table2 == None:
        return {'2024': table1}

    dict_tables = {'2023': table1, '2024': convert_to_dictionary(data=table2)}

    return dict_tables
