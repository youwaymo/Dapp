import excel_extractor as data
import sqlite3 as sqll

# function to commit and close
def commit_close(db):
    db.commit()
    db.close()

# table_labels
tl = data.get_data_from_excel()

db = sqll.connect("Db\\database.db")
cr = db.cursor()

cr.execute(f'create table if not exists Employee ({tl[0][0]} integer PRIMARY KEY UNIQUE, {tl[0][1]} text, {tl[0][2]} text, {tl[0][3]} text, {tl[0][4]} date, {tl[0][5]} text, {tl[0][6]} text, {tl[0][7]} text)')

# inserting data in Employee table
def insert_into_db():
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
    
    return True

insert_into_db()
commit_close(db)
