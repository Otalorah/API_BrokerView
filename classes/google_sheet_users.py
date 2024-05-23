import gspread

CREDENTIALS_FILE = "api-brokerview-45ca1238bc25.json"
DOCUMENT = "Usuarios BrokerView"
SHEET_NAME = "Usuarios"


class GoogleSheet_users:
    def __init__(self):
        self.gc = gspread.service_account(filename=CREDENTIALS_FILE)
        self.sh = self.gc.open(DOCUMENT)
        self.sheet = self.sh.worksheet(SHEET_NAME)

    def write_data(self, range: str, values: list[list]):
        self.sheet.update(range, values)

    def get_data_by_username(self, username: str) -> bool | list:

        cell = self.sheet.find(username)

        if not cell:
            return False

        cell_row = cell.row
        data_found = self.sheet.row_values(row=cell_row)[:8]
        return data_found

    def get_last_row_range(self) -> str:

        last_row = len(self.sheet.col_values(1)) + 1
        range_start = f"A{last_row}"
        range_end = f"H{last_row}"

        return f"{range_start}:{range_end}"

    def get_list_fondo(self) -> list:
        return self.sheet.col_values(11)[1:]

    def get_list_broker(self) -> list:
        return self.sheet.col_values(10)[1:]

    def get_users_registered(self) -> list:
        return self.sheet.col_values(8)[1:]
    
    def get_emails(self) -> list:
        return self.sheet.col_values(4)[1:]
