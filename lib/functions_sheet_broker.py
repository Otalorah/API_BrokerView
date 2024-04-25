from google_sheets.google_sheet_broker import GoogleSheet_broker


def delete_empty_fields(data_list: list[list]) -> list[list]:

    for i, row in enumerate(data_list):
        if row[1] == " ":
            return data_list[:i]

    return data_list


def convert_to_dictionary(table: list[list], table_type: str) -> list[dict]:

    table_data = list()

    COLUMNS_NAME_TABLE2 = ['MES', 'INVERSION', 'LOTE', 'GANANCIA BRUTA',
                           'GANANCIA NETA', 'COMISION', 'PORCENTAJE GANANCIA', 'RETIROS']

    if table_type == '1':
        COLUMNS_NAME_TABLE1 = ['MES', 'INVERSION', 'LOTE',
                               'GANANCIA NETA', 'COMISION', 'PORCENTAJE GANANCIA']
        for row in table:
            dict_data = {"AÑO": '2023'}

            dict_data.update(dict(zip(COLUMNS_NAME_TABLE1, row)))

            table_data.append(dict_data)

    elif table_type == '1 only':
        for row in table:
            dict_data = {"AÑO": '2024'}

            dict_data.update(dict(zip(COLUMNS_NAME_TABLE2, row)))

            table_data.append(dict_data)

    elif table_type == '2':

        for row in table:
            dict_data = {"AÑO": '2024'}

            dict_data.update(dict(zip(COLUMNS_NAME_TABLE2, row)))

            table_data.append(dict_data)

    return table_data


def get_data_sheet_broker(sheet_name: str) -> list:

    sheet = GoogleSheet_broker(sheet_name=sheet_name)

    first_table = sheet.read_first_table()
    first_table = delete_empty_fields(first_table)

    if not sheet.verify_second_table():
        return convert_to_dictionary(table=first_table, table_type='1 only')

    table1 = convert_to_dictionary(table=first_table, table_type='1')

    second_table = sheet.read_second_table()
    second_table = delete_empty_fields(second_table)

    table2 = convert_to_dictionary(table=second_table, table_type='2')

    data_list = table1 + table2

    return data_list
