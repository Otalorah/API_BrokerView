import gspread
from os import getenv
from json import loads
from dotenv import load_dotenv

load_dotenv()

CREDENTIALS = getenv('GOOGLE')
CREDENTIALS = loads(CREDENTIALS)
DOCUMENT = "FONDO INDIVIDUAL DE INVERSIÓN"


class GoogleSheet_fund:
    def __init__(self, sheet_name: str):
        self.gc = gspread.service_account_from_dict(CREDENTIALS)
        self.sh = self.gc.open(DOCUMENT)
        self.sheet = self.sh.worksheet(sheet_name)

    def get_num_rows(self) -> str:

        last_row = len(self.sheet.col_values(1))

        return f"{last_row}"

    def read_data(self) -> list[list]:

        num_rows = self.get_num_rows()
        range_values = f'A3:F{num_rows}'

        return self.sheet.get(range_name=range_values)
