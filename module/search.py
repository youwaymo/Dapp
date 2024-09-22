import sqlite3 as sqll

db = sqll.connect(r'Db\database.db')
cr = db.cursor()

def find_user(id):
    result = cr.execute('select * from Employee where Matricule = ?', (id,)).fetchone()
    if result:
        return list(result)
    else:
        return None
    
