import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('Timbres-d5e5f6ae908d.json', scope)

gc = gspread.authorize(credentials)

#sh = gc.create('A new spreadsheet')
wk = gc.open_by_key('1DUKWeNQLC6cbwkI0gntt0UrYe6WORuyMJk1kazfutgo')

sh = wk.get_worksheet(3)

cell_list = sh.range('A1:B7')
print (cell_list)
