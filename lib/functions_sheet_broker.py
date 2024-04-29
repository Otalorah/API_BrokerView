from google_sheets.google_sheet_broker import GoogleSheet_broker


def delete_empty_fields(data_list: list[list]) -> list[list]:

    for i, row in enumerate(data_list):
        if row[1] == " ":
            return data_list[:i]

    return data_list


def convert_to_dictionary(table: list[list], table_type: int) -> list[dict]:

    table_data = list()

    columns_name_table = ['mes', 'inversion', 'lote', 'ganacia_bruta',
                          'ganancia_neta', 'comision', 'porcentaje_ganancia', 'retiros']

    year_table = '2024'

    if table_type == 1:
        year_table = '2023'
        columns_name_table = ['mes', 'inversion', 'lote',
                              'ganancia_neta', 'comision', 'porcentaje_ganancia']

    for row in table:
        dict_data = {"año": year_table}

        dict_data.update(dict(zip(columns_name_table, row)))

        table_data.append(dict_data)

    return table_data


def get_data_sheet(sheet_name: str) -> list:

    sheet = GoogleSheet_broker(sheet_name=sheet_name)

    first_table = sheet.read_first_table()
    first_table = delete_empty_fields(first_table)

    # If only has one table
    if not sheet.verify_second_table():
        return convert_to_dictionary(table=first_table, table_type=2)

    table1 = convert_to_dictionary(table=first_table, table_type=1)

    second_table = sheet.read_second_table()
    second_table = delete_empty_fields(second_table)

    table2 = convert_to_dictionary(table=second_table, table_type=2)

    data_list = table1 + table2

    return data_list
