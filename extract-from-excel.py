import openpyxl as opx
from datetime import datetime

# Open The Excel File:
wb = opx.load_workbook(filename = 'Db\db.xlsx')

# Open The WorkSheet named Liste 1:
ws = wb['Liste 1']

# Initializing data list
data = []

# Fetching Data:
for row in ws.rows:
    if not row[0].value:
       break
    temp = []
    for cell in row:
        if not cell.value:
            break
        if isinstance(cell.value, datetime):
            temp.append(cell.value.strftime(f'%d/%m/%Y'))
            continue
        temp.append(cell.value)
    data.append(temp)  

