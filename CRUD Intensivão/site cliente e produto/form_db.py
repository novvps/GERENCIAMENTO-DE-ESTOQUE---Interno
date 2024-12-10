import sqlite3 as sql

con = sql.connect ('form_db.db')
cur = con.cursor()
cur.execute('DROP TABLE IF EXISTS produtos')

sql = '''CREATE TABLE "produtos" (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    NOME_PRODUTO TEXT NOT NULL,
    QUANTIDADE INTEGER NOT NULL,
    DATA_DE_COMPRA TEXT,
    DATA_DE_VALIDADE TEXT,
    VALOR_DE_COMPRA REAL,
    VALOR_DE_VENDA REAL,
    LUCRO_EM_PORCENTAGEM REAL
    )'''

cur.execute(sql)
con.commit()
con.close()