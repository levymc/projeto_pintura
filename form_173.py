from tkinter import * 
from tkinter import messagebox
import hashlib, json, sqlite3, re
from PIL import ImageTk, Image 
from datetime import datetime
import tkinter.font as font



class App(Toplevel):
    def __init__(self, user, db):
        super().__init__()
        self.db = db
        self.geometry("700x460")
        self.title('Form 173 - Solicitações')
        self.configure(background='#f0f5ff')
        self.resizable(0,0)
        self.iconbitmap(r'logo.ico')
        self.oc = StringVar()
        self.user = user
        self.fonte_fa = font.Font(family="FontAwesome", size=9)
        self.image = Image.open(r"logo.png")
        self.img = ImageTk.PhotoImage(self.image)
        try:
            banco = sqlite3.connect(self.db)
            cursor = banco.cursor()
            cursor.execute(f"SELECT codigo FROM operadores WHERE usuario='{self.user}'")
            self.cod_operador = cursor.fetchall()[0][0]
            cursor.close()
            banco.close()
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
        self.ocsAux = {}
        
        def campo_oc():
            if self.oc_campo.get() == "" or self.qnt_campo.get() == "":
                messagebox.showinfo(message="O campo de OC ou Quantidade estão vazios!")
            else:
                exist = 0
                for i in self.ocs:
                    if str(self.oc_campo.get()) in i['oc']:
                        exist = 1
                        messagebox.showinfo(message="Já tem!!")
                if exist == 0:
                    self.ocs.append({"oc":self.oc_campo.get(), "qnt": self.qnt_campo.get()})
                    self.mylistbox.insert(END, f"OC: {self.oc_campo.get()} - QNT: {self.qnt_campo.get()}" )
                    self.oc_campo.delete(0, END)
                    self.qnt_campo.delete(0, END)
                    atualizar_contador()
        
        def deletar_oc():
            selecionados = self.mylistbox.curselection()
            for selecionado in selecionados:
                s = self.mylistbox.get(selecionado)
                match = re.search(r'OC:\s*(\d+)', s)
                if match:
                    valor = match.group(1)
                    print(valor) # saída: "123"
                else:
                    print("Valor não encontrado")
                for i in self.ocs:
                    if valor in i['oc']:
                        self.ocs.remove(i)
                        print("OC removida!")
                self.mylistbox.delete(selecionado)
            atualizar_contador()

        # Pendências - Campo direito, auxiliar
        quadro = Frame(self, width = 250, height = 460, bg="#041536")
        quadro.pack(side=RIGHT)
        
        add_oc = Label(quadro, text=f"OC: ", foreground='white', background="#041536", font='Helvetica 9 bold')
        add_oc.place(x=10, y=55)
        qnt = Label(quadro, text="Qnt.: ", foreground='white', background="#041536", font='Helvetica 9 bold')
        qnt.place(x=186, y=55)
        self.oc_campo = Entry(quadro)
        self.oc_campo.place(x=55, y=55)
        self.qnt_campo = Entry(quadro)
        self.qnt_campo.place(x=220, y=55, width=20)    
        buttonAddOC = Button (quadro, font='Helvetica 8 bold', text="Adicionar OC", anchor='center', command=campo_oc,  bg='#99d199')
        buttonAddOC.place(y=90, x=160, width=80, height=22)

        y = Label(quadro, text = "OC's utilizadas no lote: ",foreground='white', background="#041536", font='Impact 15')
        y.place(x=30, y=10)
        
        def atualizar_contador():
            infoOC.config(text=f"{self.mylistbox.size()} OC's adicionadas", foreground='white', background="#041536", font='Helvetica 9 bold')

        self.mylistbox=Listbox(quadro,width=35,height=6,  font='Trebuchet 9 bold', bg='white', selectmode=SINGLE)
        self.mylistbox.place(x=35,y=150, width=190, height=250)
        infoOC = Label(quadro, text=f"{self.mylistbox.size()} OC's adicionadas", foreground='white', background="#041536", font='Helvetica 9 bold')
        infoOC.place(x=33, y=405)
        deletarOC = Button(quadro, font=self.fonte_fa, text=u"\uf1f8", anchor='center', command=deletar_oc,  bg='red', fg='black')
        deletarOC.place(x=200, y=405)

        self.mainloop()

    def insert(self, event): 
        dic = (self.cod_operador, self.numero_field.get(), self.hoje, self.cemb_field.get(), self.qnt_field.get(),self.pintor_field.get())
        
        ### CONFERINDO OS CAMPOS VAZIOS
        if (self.numero_field.get() == "" or 
            self.cemb_field.get() == "" or
            self.qnt_field.get() == "" or
            self.pintor_field.get() == ""             
        ): messagebox.showinfo(message="Preencha os campos para continuar!")
        
        elif len(self.ocs) == 0: messagebox.showinfo(message="Os campos de OC's estão vazios!")

        else: 
            x = messagebox.askquestion(title="Double-Check", message="Confirma os dados do Form_173?")
            if x == "yes":
                try:
                    banco = sqlite3.connect(self.db)
                    cursor = banco.cursor()
                    ### INSERINDO AS INFORMAÇÕES NO DB QUE SE ENCONTRA NO SERVIDOR NAS
                    cursor.execute(
                        f"""INSERT INTO form_173 (solicitante, formulario, data_solicitacao, cemb, quantidade, pintor)
                        VALUES (?,?,?,?,?,?)
                        """,(dic[0], dic[1], dic[2], dic[3], dic[4], dic[5]))
                    banco.commit()
                    id_form173 = cursor.lastrowid
                    print(id_form173)
                except Exception as ex:
                    print("133 - ",ex)
                    messagebox.showerror(message=(ex, type(ex)))

                for i in self.ocs:
                    try:  #INSERINDO AS OCS NO DB
                        text = """INSERT INTO ocs (oc, quantidade,track_form173) VALUES (?,?,?)"""
                        cursor.execute(text, (i['oc'], i['qnt'], id_form173))
                        banco.commit()
                    except Exception as ex:
                        print("form_173",ex)
                        messagebox.showerror(message=("ERRO: ",ex, type(ex)))
                    
                messagebox.showinfo(message="Informações enviadas!!")
                self.ocs = []
                
                # APAGANDO OS CAMPOS APÓS O ENVIO DAS INFO..
                self.numero_field.focus_set()
                self.numero_field.delete(0, END)
                self.pintor_field.delete(0, END)
                self.cemb_field.delete(0, END)
                self.oc_campo.delete(0, END)
                self.qnt_field.delete(0, END)
                self.qnt_campo.delete(0, END)
                self.mylistbox.delete(0, END)
                cursor.close()
                banco.close()
            else: self.numero_field.focus_set()

    def limpar(self):
        self.numero_field.focus_set()
        self.numero_field.delete(0, END)
        self.pintor_field.delete(0, END)
        self.cemb_field.delete(0, END)
        self.oc_campo.delete(0, END)
        self.qnt_field.delete(0, END)
        self.qnt_campo.delete(0, END)
        self.mylistbox.delete(0, END)

# if __name__ == "__main__":
#     app = App()
#     app.mainloop()
# App('teste')