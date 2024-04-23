import gspread

CREDENTIALS_FILE = "api-brokerview-45ca1238bc25.json"
DOCUMENT = "COPYTRADING"

gc = gspread.service_account(filename=CREDENTIALS_FILE)
sh = gc.open(DOCUMENT)
sheet = sh.worksheet('Cecilia Niño')

print(sheet.get('A1:F13'))