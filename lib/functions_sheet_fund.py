from google_sheets.google_sheet_fund import GoogleSheet_fund


def read_data_sheet(sheet_name: str) -> list[list]:

    sheet = GoogleSheet_fund(sheet_name=sheet_name)

    return sheet.read_data()


def convert_to_dictionary(data: list[list]) -> dict:

    dict_data = dict()

    num_rows = 1
    previous_row_repeated = False

    for row in data:

        cutoff_date = row[0]
        new_row = row[1:]

        if cutoff_date in dict_data:
            num_rows += 1
            dict_data[cutoff_date][num_rows] = new_row
            previous_row_repeated = True
            continue
        elif previous_row_repeated:
            num_rows = 1
            previous_row_repeated = False

        dict_data[cutoff_date] = {num_rows: new_row}

    return dict_data
