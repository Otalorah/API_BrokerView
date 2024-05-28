import gspread

CREDENTIALS_FILE = "api-brokerview-45ca1238bc25.json"
DOCUMENT = "Usuarios BrokerView"
SHEET_NAME = "Usuarios"


class GoogleSheet_users:
    def __init__(self):
        self.gc = gspread.service_account(filename=CREDENTIALS_FILE)
        self.sh = self.gc.open(DOCUMENT)
        self.sheet = self.sh.worksheet(SHEET_NAME)

    def write_data(self, range: str, values: list[list]) -> None:
        self.sheet.update(range_name=range, values=values)

    def get_data_by_username(self, username: str) -> bool | list:

        cell = self.sheet.find(username)

        if not cell:
            return False

        row = cell.row
        return self.sheet.row_values(row=row)[:8]

    def get_last_row_range(self) -> str:

        last_row = len(self.sheet.col_values(1)) + 1
        range_start = f"A{last_row}"
        range_end = f"H{last_row}"

        return f"{range_start}:{range_end}"

    def get_list_fondo(self) -> list:
        return self.sheet.col_values(12)[1:]

    def get_list_broker(self) -> list:
        return self.sheet.col_values(11)[1:]

    def get_users_registered(self) -> list:
        return self.sheet.col_values(8)[1:]

    def get_emails(self) -> list:
        return self.sheet.col_values(4)[1:]

    def get_code_email(self, email: str) -> list:

        cell = self.sheet.find(email)

        if not cell:
            return []

        cell_row = cell.row
        return self.sheet.row_values(row=cell_row)[8]

    def write_by_gmail(self, email: str, value: str, column: str) -> None:

        cell = self.sheet.find(email)
        row = cell.row

        self.sheet.update(range_name=f"{column}{row}", values=[[value]])
