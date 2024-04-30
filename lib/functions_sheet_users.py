from fastapi import HTTPException

from passlib.context import CryptContext
from passlib.hash import bcrypt

from models import models

from lib.functions_text import get_first_word

from google_sheets.google_sheet_users import GoogleSheet_users

google = GoogleSheet_users()

crypt = CryptContext(schemes=["bcrypt"])

# - - - - - - - - - - - - - - - - - - - - - Funtions Google Sheets - - - - - - - - - - - - - - - - - - - - -


def verify_user(name_sheet_user: str) -> tuple[bool]:

    list_fund = google.get_values_list_fondo()[1:]
    list_broker = google.get_values_list_broker()[1:]

    user_has_fund = name_sheet_user in list_fund
    user_has_broker = name_sheet_user in list_broker

    if not user_has_fund and not user_has_broker:
        raise HTTPException(
            status_code=406, detail='No tiene cuenta en BrokerView')

    return user_has_broker, user_has_fund


def create_user_sheet(user: models.UserCreate) -> tuple[str, bool, bool]:

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
    user_data.append(name_sheet_user)

    user_values = [user_data]

    range = google.get_last_row_range()
    google.write_data(range=range, values=user_values)

    return user_dict["username"], user_has_broker, user_has_fondo, name_sheet_user


def get_data_user(username: str) -> bool | list:

    list_data = google.get_data_by_username(username=username)

    if not list_data:
        return False

    list_fields = ['username', 'name', 'lastname',
                   'email', 'password', 'has_fund', 'has_broker', 'user_sheet']
    dict_data = dict(zip(list_fields, list_data))

    return dict_data


def verify_password(username: str, password: str) -> bool:

    list_data_user = get_data_user(username=username)
    password_in_sheet = list_data_user['password']

    if bcrypt.verify(password, password_in_sheet):
        return True
    return False
