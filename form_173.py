from tkinter import * 
from tkinter import messagebox
import hashlib, json, sqlite3
from PIL import ImageTk, Image 
from datetime import datetime

try:
    banco = sqlite3.connect(r'//NasTecplas/Pintura/DB/pintura.db')
    cursor = banco.cursor()
except Exception as ex: messagebox.showerror(message=(ex, type(ex)))

class App(Toplevel):
    def __init__(self, user):
        super().__init__()
        self.geometry("700x460")
        self.title('Form 173 - Solicitações')
        self.configure(background='#f0f5ff')
        self.resizable(0,0)
        self.iconbitmap(r'logo.ico')
        self.oc = StringVar()
        self.user = user
        self.image = Image.open(r"logo.png")
        self.img = ImageTk.PhotoImage(self.image)
        try:
            cursor.execute(f"SELECT codigo FROM operadores WHERE usuario='{self.user}'")
            self.cod_operador = cursor.fetchall()[0][0]
        except Exception as ex: messagebox.showerror(message=(ex, type(ex)))

        self.create_wigets()

    def create_wigets(self):
        # Form 173 - Campo Principal
        q1 = Frame(self, width = 700, height = 40, background="#f0f5ff")
        q1.place(x=0,y=0)
        x = Label(q1, text="Form. 173 - Solicitação de Preparação de Tinta", font='Impact 16', foreground='black', background='#f0f5ff')
        x.place(x=20, y=10)
        img_frame = Label(self,image=self.img, background='#f0f5ff')
        img_frame.place(x=0, y=399)
        solicitante = Label(self, text="Solicitante\n(Requesting Person)", font='Helvetica 9 bold', foreground='#011336', background='#f0f5ff')
        solicitante.place(x=40, y=60)
        self.solicitante_field = Label(self, text=self.user+" - "+str(self.cod_operador), font='Helvetica 9 bold', foreground='#011336', background='#f0f5ff')
        self.solicitante_field.place(x=190, y=60)
        numero = Label(self, text="Formulário Nº\n(Form Nº)", font='Helvetica 9 bold', foreground='#011336', background='#f0f5ff')
        numero.place(x=40, y=120)
        self.numero_field = Entry(self)
        self.numero_field.place(x=190, y=120, width=150, height=30)
        pintor = Label(self, text="Pintor\n(Painter)", font='Helvetica 10 bold', foreground='#011336', background='#f0f5ff')
        pintor.place(x=40, y=180)
        self.hoje = datetime.today().strftime('%d-%m-%Y')
        self.agora = datetime.today().strftime('%d-%m-%Y %H:%M')
        self.pintor_field = Entry(self)
        self.pintor_field.place(x=190, y=180, width=150, height=30)
        cemb = Label(self, text="CEMB Tinta\n(Paint CODE)", font='Helvetica 9 bold', foreground='#011336', background='#f0f5ff')
        cemb.place(x=40, y=240)
        self.cemb_field = Entry(self)
        self.cemb_field.place(x=190, y=240, width=150, height=30)
        qnt = Label(self, text="Quantidade Solicitada\n(Quantity Requested)", font='Helvetica 9 bold', foreground='#011336', background='#f0f5ff')
        qnt.place(x=40, y=300)
        self.qnt_field = Entry(self)
        self.qnt_field.place(x=190, y=300, width=150, height=30)
        g_ml = Label(self, text="g ou ml", font='Helvetica 8 bold', foreground='#011336', background='#f0f5ff')
        g_ml.place(x=345, y=310)
        botao = Button(self, text="Enviar Solicitação")
        botao.bind('<Button-1>', self.insert)
        botao.place(x=330, y=370,height=30)
        limpar = Button(self, text="Limpar Dados", command=self.limpar)
        limpar.place(x=195, y=370,height=30)

        self.numero_ocs = 0
        self.y = 50
        self.ocs = []
        self.ocs_label = []
        self.contador = 0
        def campo_oc():
            if self.contador == 0:
                add_oc = Label(quadro, text=f"{self.numero_ocs+1}ª OC: ", foreground='white', background="#041536", font='Helvetica 9 bold')
                add_oc.place(x=10, y=self.y)
                qnt = Label(quadro, text="Qnt.: ", foreground='white', background="#041536", font='Helvetica 9 bold')
                qnt.place(x=186, y=self.y)
                self.oc_campo = Entry(quadro)
                self.oc_campo.place(x=55, y=self.y)
                self.qnt_campo = Entry(quadro)
                self.qnt_campo.place(x=220, y=self.y, width=20)
                self.ocs_label.append((add_oc, qnt))
                self.ocs.append((self.oc_campo, self.qnt_campo))
                self.y+=40
                self.numero_ocs +=1
                self.contador += 1
            
        
        def delete_campo_oc(event):
            try:
                self.ocs[-1][0].place_forget()
                self.ocs[-1][1].place_forget()
                self.ocs_label[-1][0].place_forget()
                self.ocs_label[-1][1].place_forget()
                if not self.numero_ocs == 0:
                    self.y -= 40
                    self.numero_ocs -= 1
                    self.ocs.remove((self.ocs[-1][0],self.ocs[-1][1]))
                    self.ocs_label.remove((self.ocs_label[-1][0], self.ocs_label[-1][1]))
            except Exception as ex: print(ex)

        # Pendências - Campo direito, auxiliar
        quadro = Frame(self, width = 250, height = 460, bg="#041536")
        quadro.pack(side=RIGHT)
        
        add_oc = Label(quadro, text=f"OC: ", foreground='white', background="#041536", font='Helvetica 9 bold')
        add_oc.place(x=10, y=50)
        qnt = Label(quadro, text="Qnt.: ", foreground='white', background="#041536", font='Helvetica 9 bold')
        qnt.place(x=186, y=50)
        self.oc_campo = Entry(quadro)
        self.oc_campo.place(x=55, y=50)
        self.qnt_campo = Entry(quadro)
        self.qnt_campo.place(x=220, y=50, width=20)    
        buttonAddOC = Button (quadro, font='Helvetica 8 bold', text="Adicionar OC", anchor='center', command=campo_oc, bg='#99d199')
        buttonAddOC.place(y=90, x=160, width=80, height=22)

        y = Label(quadro, text = "OC's utilizadas no lote: ",foreground='white', background="#041536", font='Impact 15')
        y.place(x=30, y=10)

        self.mainloop()

    def insert(self, event): 
        dic = (self.cod_operador, self.numero_field.get(), self.hoje, self.cemb_field.get(), self.qnt_field.get(),self.pintor_field.get())

        ### CONFERINDO OS CAMPOS VAZIOS
        cont = 0
        for i in range(len(self.ocs)):
            if self.ocs[i][0].get() != '':
                cont += 1
        if (self.numero_field.get() == "" and 
            self.cemb_field.get() == "" and
            self.qnt_field.get() == "" and
            self.pintor_field.get() == ""             
        ): messagebox.showinfo(message="Os campos estão vazios!")
        elif cont == 0: messagebox.showinfo(message="Os campos de OC's estão vazios!")

        else: 
            x = messagebox.askquestion(title="Double-Check", message="Confirma os dados do Form_173?")
            if x == "yes":
                try:
                    ### INSERINDO AS INFORMAÇÕES NO DB QUE SE ENCONTRA NO SERVIDOR NAS
                    cursor.execute(
                        f"""INSERT INTO form_173 (solicitante, formulario, data_solicitacao, cemb, quantidade, pintor)
                        VALUES (?,?,?,?,?,?)
                        """,(dic[0], dic[1], dic[2], dic[3], dic[4], dic[5]))
                    cursor.execute("""SELECT rowid FROM form_173 WHERE rowid=(SELECT MAX(rowid) FROM form_173)""")
                    id_form173 = cursor.fetchone()[0] #Retorna o ID da última linha
                    banco.commit()
                except Exception as ex: messagebox.showerror(message=(ex, type(ex)))

                for i in self.ocs:
                    if not i[0] == "":
                        try:  #INSERINDO AS OCS NO DB
                            text = """INSERT INTO ocs (oc, quantidade,track_form173) VALUES (?,?,?)"""
                            cursor.execute(text, [i[0].get(), i[1].get(), id_form173])
                            banco.commit()
                        except Exception as ex: messagebox.showerror(message=(ex, type(ex)))
                
                # APAGANDO OS CAMPOS APÓS O ENVIO DAS INFO..
                self.numero_field.focus_set()
                self.numero_field.delete(0, END)
                self.pintor_field.delete(0, END)
                self.cemb_field.delete(0, END)
                self.qnt_field.delete(0, END)
                for i in self.ocs:
                    i[0].focus_set()
                    i[0].delete(0,END)
                    i[1].focus_set()
                    i[1].delete(0,END)
                self.numero_field.focus_set()  
                self.destroy()
            else: self.numero_field.focus_set()

    def limpar(self):
        self.numero_field.focus_set()
        self.numero_field.delete(0, END)
        self.pintor_field.delete(0, END)
        self.cemb_field.delete(0, END)
        self.qnt_field.delete(0, END)
        for i in self.ocs:
            i[0].focus_set()
            i[0].delete(0,END)
            i[1].focus_set()
            i[1].delete(0,END)
        self.numero_field.focus_set()

# if __name__ == "__main__":
#     app = App()
#     app.mainloop()
# App('teste')