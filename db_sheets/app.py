from google_sheet_actions import GoogleSheet

file_name_gs = r"C:\Users\juanm\OneDrive\Desktop\Otalorin\BrokerView Proyect\API BrokerView\db_sheets\api-brokerview-45ca1238bc25.json"
google_sheet = "Usuarios BrokerView"
sheet_name = "Hoja 1"


#Init
google = GoogleSheet(file_name=file_name_gs, document=google_sheet, sheet_name=sheet_name)

value =[['Juan Camilo','Camilo','Otálora Hernández','camilo@gmail.com','cxmilx','12345']]
range = google.get_last_row_range()
google.write_data(range=range,values=value)

# import os
# cwd = os.getcwd()
# print("Directorio actual:", cwd)
# ruta_absoluta = os.path.abspath("api-brokerview-45ca1238bc25.json")
# print("Ruta absoluta del archivo de credenciales:", ruta_absoluta)