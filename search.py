from extract_from_excel import get_data_from_excel as data
import sqlite3 as sqll

# function to commit and close
def commit_close(db):
    db.commit()
    db.close()

# table_labels
tl = data()

db = sqll.connect(r'Db\database.db')
cr = db.cursor()

cr.execute(f'create table if not exists Employee ({tl[0][0]} integer PRIMARY KEY UNIQUE, {tl[0][1]} text, {tl[0][2]} text, {tl[0][3]} text, {tl[0][4]} date, {tl[0][5]} text, {tl[0][6]} text, {tl[0][7].split()[0]}_{tl[0][7].split()[1]} text)')

# inserting data in Employee table
for v in tl[1:]:
    if(v[3] == 'C'):
        v[3] = 'Cheikh Urbain 2eme grade'
    elif(v[3] == 'M2'):
        v[3] = 'Moqaddem Urbain 2eme grade'
    elif(v[3] == 'M1'):
        v[3] = 'Moqaddem Urbain 1ere grade'
    elif(v[3] == 'A'):
        v[3] = 'Arifa Urbain'
        
    cr.execute('insert into Employee values(?,?,?,?,?,?,?,?)', (v[0],v[1],v[2],v[3],v[4],v[5],v[6],v[7]))

commit_close(db)
