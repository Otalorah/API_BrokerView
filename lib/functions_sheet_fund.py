from google_sheets.google_sheet_fund import GoogleSheet_fund


def get_data_sheet(sheet_name: str) -> list[list]:

    sheet = GoogleSheet_fund(sheet_name=sheet_name)
    return sheet.read_data()


def convert_to_dictionary(data: list[list]) -> list[dict]:

    list_data = list()
    COLUMNS_NAME = ['fecha_corte', 'aporte', 'fecha_de_aporte',
                    'saldo_anterior', 'rendimientos', 'saldo_actual']

    for row in data:
        list_data.append(dict(zip(COLUMNS_NAME, row)))

    return list_data
