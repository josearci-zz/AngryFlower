import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('Timbres-d5e5f6ae908d.json', scope)

gc = gspread.authorize(credentials)

#sh = gc.create('A new spreadsheet')
wk = gc.open_by_key('1owXgS0qF0ER_kvOEk_IjyALF_jvMPyIU4umi5kO5Azo')

sh = wk.get_worksheet(0)

cell_list = sh.range('g4:g80')
print (cell_list)
