from google_sheets.google_sheet_fund import GoogleSheet_fund


def read_data_sheet(sheet_name: str) -> list[list]:

    sheet = GoogleSheet_fund(sheet_name=sheet_name)
    return sheet.read_data()


def convert_to_dictionary(data: list[list]) -> list[dict]:

    list_data = list()
    COLUMNS_NAME = ['FECHA CORTE', 'APORTE', 'FECHA DE APORTE',
                    'SALDO ANTERIOR', 'RENDIMIENTOS', 'SALDO ACTUAL']

    for row in data:
        list_data.append(dict(zip(COLUMNS_NAME, row)))

    return list_data
