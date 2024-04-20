from extract_from_excel import get_data_from_excel as gdfe
import sqlite3 as sqll

# table_labels
tl = gdfe()[0]

db = sqll.connect(r'Db\database.db')
cr = db.cursor()

cr.execute(f'create table if not exists Employee ({tl[0]} integer PRIMARY KEY UNIQUE, {tl[1]} text, {tl[2]} text, {tl[3]} text, {tl[4]} date, {tl[5]} text, {tl[6]} text, {tl[7].split()[0]}_{tl[7].split()[1]} text)')

db.commit()
db.close()
