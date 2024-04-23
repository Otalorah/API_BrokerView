from google_sheets.google_sheet_broker import GoogleSheet_broker


def delete_empty_fields(data_list: list[list]) -> list[list]:

    for i, row in enumerate(data_list):
        if row[1] == " ":
            return data_list[:i]

    return data_list


def get_data_sheet_broker(sheet_name: str) -> tuple[list]:

    sheet = GoogleSheet_broker(sheet_name=sheet_name)

    first_table = sheet.read_first_table()
    first_table = delete_empty_fields(first_table)
    second_table = None

    if sheet.verify_second_table():
        second_table = sheet.read_second_table()
        second_table = delete_empty_fields(second_table)

    return first_table, second_table


def convert_to_dictionary(data: list[list]) -> dict:

    dict_data = dict()

    for row in data:

        month = row[0]
        new_row = row[1:]

        dict_data[month] = new_row

    return dict_data
