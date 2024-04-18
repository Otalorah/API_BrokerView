import gspread

class GoogleSheet:
    def __init__(self, file_name, document, sheet_name):
        self.gc = gspread.service_account(filename=file_name)
        self.sh = self.gc.open(document)
        self.sheet = self.sh.worksheet(sheet_name)

    def write_data(self, range: str, values: list[list]):
        self.sheet.update(range, values)

    def get_data_by_username(self, username: str) -> bool | list :

        cell = self.sheet.find(username)

        if not cell:
            return False
        
        cell_row = cell.row
        data_found = self.sheet.row_values(row=cell_row)[:7]
        return data_found

    def get_last_row_range(self) -> str:
        
        last_row = len(self.sheet.col_values(1)) + 1
        range_start = f"A{last_row}"
        range_end = f"G{last_row}"

        return f"{range_start}:{range_end}"

    def get_values_list_fondo(self) -> list:
        return self.sheet.col_values(10)
    
    def get_values_list_broker(self) -> list:
        return self.sheet.col_values(9)