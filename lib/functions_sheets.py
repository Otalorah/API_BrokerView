from models import models

from lib.google_sheet_class import GoogleSheet

CREDENTIALS_FILE = "api-brokerview-45ca1238bc25.json"
DOCUMENT = "Usuarios BrokerView"
SHEET_NAME = "Usuarios"

google = GoogleSheet(file_name=CREDENTIALS_FILE, document=DOCUMENT, sheet_name=SHEET_NAME)

def create_user_sheet(user:models.UserCreate) -> str:
    user_dict = dict(user)
    values = [valor for valor in user_dict.values()]
    values = [values]

    range = google.get_last_row_range()
    google.write_data(range=range,values=values)

    return user_dict["username"]