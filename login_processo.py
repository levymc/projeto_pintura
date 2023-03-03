from tkinter import *
from tkinter import messagebox
import hashlib, sqlite3, form_40
from datetime import timedelta
from datetime import datetime

class Login(Toplevel):
    def __init__(self, db, dados, id_form173):
        self.db = db
        self.dados = dados
        self.id_form173 = id_form173
        super().__init__()
        self.title("LOGIN") 
        self.geometry("260x130")
        self.configure(bg='white')
        self.iconbitmap(r'logo.ico')
        self.resizable(0,0)
        self.log()

    def log(self):
        u = Label(self, text="Usuário: ", bg="white")
        u.place(x=10, y=20) 
        self.usuario = StringVar()
        self.usuario = Entry(self, textvariable=self.usuario, bg='white') 
        # self.usuario.bind("<Return>", usuario.focus_set) 
        self.usuario.place(x=70, y=20, width=140)
        s = Label(self, text="Senha: ", bg="white")
        s.place(x=10, y= 50)
        self.senha = StringVar()
        self.senha = Entry(self, textvariable=self.senha, show='*', bg='white') 
        # self.senha.bind("<Return>", senha.focus_set) 
        self.senha.place(x=70, y=50, width=140)
        self.bind('<Return>',self.confere)
        submit = Button(self, text="Logar", fg="white",bg="black", width=8) 
        submit.bind('<Button-1>', self.confere)
        submit.place(x=160, y=80)
        img = PhotoImage(file=r'mini_logo.png')
        img_frame = Label(self, image=img, background='#f0f5ff')
        img_frame.place(x=0,y=100)
        self.mainloop()

    def confere(self, event):
        user = self.usuario.get()
        password = self.senha.get()
        s = hashlib.md5(password.encode()).hexdigest()
        try:
            banco = sqlite3.connect(self.db)
            cursor = banco.cursor()
        except: messagebox.showerror(message="Error ao conctar no DB")
        try:
            dados = cursor.execute(f"SELECT senha FROM operadores WHERE usuario='{user}'").fetchall()[0][0]
            dados2 = cursor.execute(f"SELECT usuario FROM operadores WHERE senha='{s}'").fetchall()[0][0]
            if dados and dados2:
                priority = cursor.execute(f"SELECT priority FROM operadores WHERE usuario='{user}'").fetchall()[0][0]
                codigoProcesso = cursor.execute(f"SELECT codigo FROM operadores WHERE usuario='{user}'").fetchall()[0][0]
                if priority == 'admin':
                    self.destroy()
                    cursor.close()
                    banco.close()
                    print(self.dados)
                    insert(self.dados, self.db, self.id_form173, codigoProcesso)
                else:
                    messagebox.showerror(message="Usuário sem permissão!")
            else:
                messagebox.showerror(message="Usuário ou senha inválidos!")
        except: messagebox.showerror(message="Algum erro aconteceu")

def insert(dados, db, id_form173, codigoProcesso):
    try:
        banco = sqlite3.connect(db)
        cursor = banco.cursor()
        x = messagebox.askquestion(title="Double-Check", message="Confirma o Envio dos Dados??")
        if x=='yes':
            try:                                                                                                       
                    cursor.execute("""INSERT INTO form_40 (mescla, data_prep, temperatura, umidade, cod_mp, lotemp, shelf_life, ini_agitador, ini_mistura, ini_diluentes, viscosidade, proporcao, ini_adequacao, ini_inducao, pot_life, responsavel, Id_form173)
                            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                    """, (dados[0],dados[1],dados[2],dados[3],dados[4],dados[5],dados[6],dados[7] ,dados[8],dados[9],dados[10],dados[11],dados[12],dados[13],dados[14], codigoProcesso, id_form173))
                    cursor.execute("INSERT INTO form_161 (track_form173, print) VALUES(?,?)", (id_form173, 0))
            except Exception as ex: messagebox.showerror(message=ex)
            if not dados[13] == '':
                    (h,m) = dados[13].split(':')
                    term_inducao = timedelta(hours=int(h), minutes=int(m)+30)
                    term_inducao = str(term_inducao)[:-3]
                    cursor.execute(f"UPDATE form_40 SET term_inducao='{str(term_inducao)}' WHERE mescla='{dados[0]}'")
                    banco.commit()
                    # except ValueError: 
                    #         messagebox.showinfo(message='O horário de "Indução" foi digitado errôneamente')
                    #         # cursor.execute(f"DELETE FROM form_40 WHERE mescla='{dados[0]}'")
            if not dados[12] == '':
                    if not dados[12] == r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$':
                            messagebox.showinfo(message='O valor digitado para "Início da Adequação" está no formato errado!')
                    else:
                            (h,m) = dados[12].split(':')
                            term_adequacao = timedelta(hours=int(h), minutes=int(m)+12)
                            term_adequacao = str(term_adequacao)[:-3]
                            # cursor.execute("INSERT INTO form_40 (term_adequacao) VALUES (?)", str(term_adequcao))
                            cursor.execute(f"UPDATE form_40 SET term_adequacao='{str(term_adequacao)}' WHERE mescla='{dados[0]}'")
                            banco.commit()
            if not dados[9] == '':
                    (h,m) = dados[9].split(':')
                    ter_diluentes = timedelta(hours=int(h), minutes=int(m)+12)
                    ter_diluentes = str(ter_diluentes)[:-3]
                    cursor.execute(f"UPDATE form_40 SET ter_diluentes='{str(ter_diluentes)}' WHERE mescla='{dados[0]}'")
                    banco.commit()
            if not dados[8] == '':
                    (h,m) = dados[8].split(':')
                    ter_mistura = timedelta(hours=int(h), minutes=int(m)+12)
                    ter_mistura = str(ter_mistura)[:-3]
                    cursor.execute(f"UPDATE form_40 SET ter_mistura='{str(ter_mistura)}' WHERE mescla='{dados[0]}'")
                    banco.commit()
            if not dados[7] == '':
                    (h,m) = dados[7].split(':')
                    ter_agitador = timedelta(hours=int(h), minutes=int(m)+12)
                    ter_agitador = str(ter_agitador)[:-3]
                    cursor.execute(f"UPDATE form_40 SET ter_agitador='{str(ter_agitador)}' WHERE mescla='{dados[0]}'")
                    banco.commit()
            cursor.execute(f"UPDATE form_40 SET excessao=1 WHERE mescla='{dados[0]}'")
            banco.commit()
            cursor.close()
            banco.close()
    except Exception as ex: messagebox.showerror(message=["Erro: ", ex, type(ex)])

# if __name__ == "__main__":
#     log = Login()
