import gspread
from os import getenv
from json import loads
from dotenv import load_dotenv

load_dotenv()

CREDENTIALS = getenv('GOOGLE')
CREDENTIALS = loads(CREDENTIALS)
DOCUMENT = "COPYTRADING"


class GoogleSheet_broker:
    def __init__(self, sheet_name: str):
        self.gc = gspread.service_account_from_dict(CREDENTIALS)
        self.sh = self.gc.open(DOCUMENT)
        self.sheet = self.sh.worksheet(sheet_name)

    def read_first_table(self) -> list[list]:

        if not bool(self.sheet.col_values(10)):
            return self.sheet.get('A2:H13')

        return self.sheet.get('A2:F13')

    def verify_second_table(self) -> bool:
        return bool(self.sheet.col_values(10))

    def read_second_table(self) -> list[list]:
        return self.sheet.get('J2:Q13')
