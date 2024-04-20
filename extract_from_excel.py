import openpyxl as opx
from datetime import datetime

# Initializing data list
data = []

# Fetching Data:
def get_data_from_excel(filepath = r'Db\db.xlsx', ws = 'Liste 1'):
    # Open The Excel File:
    wb = opx.load_workbook(filename = filepath)

    # Open The WorkSheet named Liste 1:
    ws = wb['Liste 1']

    for row in ws.rows:
        # Eliminate blank rows
        if not row[0].value:
            break
        temp = []
        for cell in row:
            # Eliminate blank Cells
            if not cell.value:
                break
            # Formating Date
            if isinstance(cell.value, datetime):
                temp.append(cell.value.strftime(f'%d/%m/%Y'))
                continue
            temp.append(cell.value)
        data.append(temp)  
    
    wb.close()

    return data
