import gspread

CREDENTIALS_FILE = "api-brokerview-45ca1238bc25.json"
DOCUMENT = "COPYTRADING"


class GoogleSheet_broker:
    def __init__(self, sheet_name: str):
        self.gc = gspread.service_account(filename=CREDENTIALS_FILE)
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
