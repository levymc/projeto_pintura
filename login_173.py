from tkinter import *
from tkinter import messagebox
import hashlib, sqlite3
import json
import main, form_173

class Login(Toplevel):
    def __init__(self):
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
        print(user,password)
        s = hashlib.md5(password.encode()).hexdigest()
        try:
            banco = sqlite3.connect(r'//NasTecplas/Public/Levy/dig_pintura/pintura.db')
            cursor = banco.cursor()
        except: messagebox.showerror(message="Error ao conctar no DB")
        try:
            cursor.execute(f"SELECT * FROM operadores WHERE usuario = '{user}' AND senha = '{s}'")
            conteudo = cursor.fetchall()[0]
            self.destroy()
            form_173.App(user)
            print(conteudo)
        except: messagebox.showerror(message="Usuário ou senha inválidos!")

# if __name__ == "__main__":
#     log = Login()
