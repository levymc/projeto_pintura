import sqlite3

db = r"pintura.db"

def conteudoForm173_pendente():
    banco = sqlite3.connect(db)
    cursor = banco.cursor()
    conteudo = cursor.execute(f"SELECT * FROM form_173 WHERE pendencia=1").fetchall()
    return conteudo

# print(conteudoForm173_pendente())