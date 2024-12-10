import sqlite3 as sql
try:
    con = sql.connect ('users_db.db')
    cur = con.cursor()
    cur.execute('DROP TABLE IF EXISTS users')

    sql = '''CREATE TABLE "users" (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        NOME VARCHAR(250) NOT NULL,
        SENHA VARCHAR(40) NOT NULL,
        EMAIL VARCHAR(300) NOT NULL,
        CPF VARCHAR(11) UNIQUE NOT NULL

        )'''

    cur.execute(sql)
    con.commit()
    con.close()
except:
    print("falha")