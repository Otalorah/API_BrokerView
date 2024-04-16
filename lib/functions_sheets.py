from fastapi import HTTPException

from passlib.context import CryptContext
from passlib.hash import bcrypt

from models import models

from lib.functions_text import get_first_word

from lib.google_sheet_class import GoogleSheet

CREDENTIALS_FILE = "api-brokerview-45ca1238bc25.json"
DOCUMENT = "Usuarios BrokerView"
SHEET_NAME = "Usuarios"

google = GoogleSheet(file_name=CREDENTIALS_FILE, document=DOCUMENT, sheet_name=SHEET_NAME)

crypt = CryptContext(schemes=["bcrypt"])

# - - - - - - - - - - - - - - - - - - - - - Funtions Google Sheets - - - - - - - - - - - - - - - - - - - - -


def verify_user(name_sheet_user: str) -> tuple[bool]:

    list_fondo = google.get_values_list_fondo()[1:]
    list_broker = google.get_values_list_broker()[1:]

    if not name_sheet_user in list_fondo and not name_sheet_user in list_broker:
        raise HTTPException(
            status_code=406, detail='No tiene cuenta en BrokerView')

    user_has_fondo = False
    user_has_broker = False

    if name_sheet_user in list_fondo:
        user_has_fondo = True

    if name_sheet_user in list_broker:
        user_has_broker = True

    return user_has_broker, user_has_fondo


def create_user_sheet(user:models.UserCreate) -> tuple[str,bool,bool]:

    user_dict = dict(user)

    name_sheet_user = get_first_word(
        user_dict["name"]) + ' ' + get_first_word(user_dict["lastname"])

    user_has_broker, user_has_fondo = verify_user(name_sheet_user)

    # The user is verify

    hashed_password = bcrypt.hash(user.password)

    user_dict['password'] = hashed_password

    user_data = [valor for valor in user_dict.values()]
    user_data.append(user_has_fondo)
    user_data.append(user_has_broker)

    user_values = [user_data]

    range = google.get_last_row_range()
    google.write_data(range=range, values=user_values)

    return user_dict["username"], user_has_broker, user_has_fondo

def get_data_user_sheet(username:str) -> bool | list :
    return google.get_data_by_username(username=username)

def verify_password(username:str, password:str) -> bool:

    list_data_user = get_data_user_sheet(username=username)
    password_in_sheet = list_data_user[4]

    if bcrypt.verify(password, password_in_sheet):
        return True
    return False