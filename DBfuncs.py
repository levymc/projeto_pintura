import sqlite3
from tkinter import messagebox

db = r"pintura.db"

def conteudoForm173_pendente():
    banco = sqlite3.connect(db)
    cursor = banco.cursor()
    conteudo = cursor.execute(f"SELECT * FROM form_173 WHERE pendencia=1").fetchall()
    cursor.close()
    banco.close()
    return conteudo

def insertOC(id_form173, ocs):
    banco = sqlite3.connect(db)
    cursor = banco.cursor()
    print("AQUIII", ocs)
    for i in ocs:
        try:
            cursor.execute(f"INSERT INTO ocs (oc, quantidade,track_form173) VALUES (?,?,?)",
                           (i['oc'], i['qnt'], id_form173))
        except Exception as e:messagebox.showerror(message=f"Erro: {e} - {type(e)}")
    banco.commit()
    cursor.close()
    banco.close()

# print(conteudoForm173_pendente())