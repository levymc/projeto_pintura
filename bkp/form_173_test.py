from tkinter import * 
from tkinter import messagebox
from tkinter.ttk import *
import hashlib, json, sqlite3
from PIL import ImageTk, Image 
from datetime import datetime

try:
    banco = sqlite3.connect(r'//NasTecplas/Public/Levy/dig_pintura/pintura.db')
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
        self.user = user
        self.image = Image.open(r"logo.png")
        self.img = ImageTk.PhotoImage(self.image)
        try:
            cursor.execute(f"SELECT codigo FROM operadores WHERE usuario='{self.user}'")
            self.cod_operador = cursor.fetchall()[0][0]
        except Exception as ex: messagebox.showerror(message=(ex, type(ex)))

        self.create_wigets()

    def create_wigets(self):
        # Definindo os estilos
        s1  = Style()
        s1.configure("s1.TFrame",background="#f0f5ff")
        s2  = Style()
        s2.configure("s2.TFrame",background="#041536", foreground="white")
        s3  = Style()
        s3.configure("s3.TFrame",background="#f0f5ff")

        # Form 173 - Campo Principal
        q1 = Frame(self, width = 700, height = 40, style='s1.TFrame')
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

        # Pendências - Campo direito, auxiliar
        quadro = Frame(self, width = 250, height = 460, style='s2.TFrame')
        quadro.pack(side=RIGHT)
        y = Label(quadro, text = "OC's utilizadas no lote: ",foreground='white', background="#041536", font='Impact 15')
        y.place(x=30, y=10)
        oc1 = Label(quadro, text = "OC 1: ", foreground='white', background="#041536", font='Helvetica 9 bold')
        oc1.place(x=10,y=50)
        self.oc1_field = Entry(quadro)
        self.oc1_field.place(x=55,y=50)
        qnt1 = Label(quadro, text="Qnt.: ", foreground='white', background="#041536", font='Helvetica 9 bold')
        qnt1.place(x=186, y=50)
        self.qnt1_field = Entry(quadro)
        self.qnt1_field.place(x=220, y=50, width=20)
        oc2 = Label(quadro, text = "OC 2: ", foreground='white', background="#041536", font='Helvetica 9 bold')
        oc2.place(x=10,y=90)
        self.oc2_field = Entry(quadro)
        self.oc2_field.place(x=55,y=90)
        qnt2 = Label(quadro, text="Qnt.: ", foreground='white', background="#041536", font='Helvetica 9 bold')
        qnt2.place(x=186, y=90)
        self.qnt2_field = Entry(quadro)
        self.qnt2_field.place(x=220, y=90, width=20)
        oc3 = Label(quadro, text = "OC 3: ", foreground='white', background="#041536", font='Helvetica 9 bold')
        oc3.place(x=10,y=130)
        self.oc3_field = Entry(quadro)
        self.oc3_field.place(x=55,y=130)
        qnt3 = Label(quadro, text="Qnt.: ", foreground='white', background="#041536", font='Helvetica 9 bold')
        qnt3.place(x=186, y=130)
        self.qnt3_field = Entry(quadro)
        self.qnt3_field.place(x=220, y=130, width=20)
        oc4 = Label(quadro, text = "OC 4: ", foreground='white', background="#041536", font='Helvetica 9 bold')
        oc4.place(x=10,y=170)
        self.oc4_field = Entry(quadro)
        self.oc4_field.place(x=55,y=170)
        qnt4 = Label(quadro, text="Qnt.: ", foreground='white', background="#041536", font='Helvetica 9 bold')
        qnt4.place(x=186, y=170)
        self.qnt4_field = Entry(quadro)
        self.qnt4_field.place(x=220, y=170, width=20)
        oc4 = Label(quadro, text = "OC 5: ", foreground='white', background="#041536", font='Helvetica 9 bold')
        oc4.place(x=10,y=210)
        self.oc5_field = Entry(quadro)
        self.oc5_field.place(x=55,y=210)
        qnt5 = Label(quadro, text="Qnt.: ", foreground='white', background="#041536", font='Helvetica 9 bold')
        qnt5.place(x=186, y=210)
        self.qnt5_field = Entry(quadro)
        self.qnt5_field.place(x=220, y=210, width=20)
        oc6 = Label(quadro, text = "OC 6: ", foreground='white', background="#041536", font='Helvetica 9 bold')
        oc6.place(x=10,y=250)
        self.oc6_field = Entry(quadro)
        self.oc6_field.place(x=55,y=250)
        qnt6 = Label(quadro, text="Qnt.: ", foreground='white', background="#041536", font='Helvetica 9 bold')
        qnt6.place(x=186, y=250)
        self.qnt6_field = Entry(quadro)
        self.qnt6_field.place(x=220, y=250, width=20)
        oc7 = Label(quadro, text = "OC 7: ", foreground='white', background="#041536", font='Helvetica 9 bold')
        oc7.place(x=10,y=290)
        self.oc7_field = Entry(quadro)
        self.oc7_field.place(x=55,y=290)
        qnt7 = Label(quadro, text="Qnt.: ", foreground='white', background="#041536", font='Helvetica 9 bold')
        qnt7.place(x=186, y=290)
        self.qnt7_field = Entry(quadro)
        self.qnt7_field.place(x=220, y=290, width=20)
        oc8 = Label(quadro, text = "OC 8: ", foreground='white', background="#041536", font='Helvetica 9 bold')
        oc8.place(x=10,y=330)
        self.oc8_field = Entry(quadro)
        self.oc8_field.place(x=55,y=330)
        qnt8 = Label(quadro, text="Qnt.: ", foreground='white', background="#041536", font='Helvetica 9 bold')
        qnt8.place(x=186, y=330)
        self.qnt8_field = Entry(quadro)
        self.qnt8_field.place(x=220, y=330, width=20)
        oc9 = Label(quadro, text = "OC 9: ", foreground='white', background="#041536", font='Helvetica 9 bold')
        oc9.place(x=10,y=370)
        self.oc9_field = Entry(quadro)
        self.oc9_field.place(x=55,y=370)
        qnt9 = Label(quadro, text="Qnt.: ", foreground='white', background="#041536", font='Helvetica 9 bold')
        qnt9.place(x=186, y=370)
        self.qnt9_field = Entry(quadro)
        self.qnt9_field.place(x=220, y=370, width=20)
        oc10 = Label(quadro, text = "OC 10: ", foreground='white', background="#041536", font='Helvetica 9 bold')
        oc10.place(x=10,y=410)
        self.oc10_field = Entry(quadro)
        self.oc10_field.place(x=55,y=410)
        qnt10 = Label(quadro, text="Qnt.: ", foreground='white', background="#041536", font='Helvetica 9 bold')
        qnt10.place(x=186, y=410)
        self.qnt10_field = Entry(quadro)
        self.qnt10_field.place(x=220, y=410, width=20)
        self.mainloop()

    def insert(self, event): 
        dic = (self.cod_operador, self.numero_field.get(), self.hoje, self.cemb_field.get(), self.qnt_field.get(),self.pintor_field.get())
        dic_oc = ((str(self.oc1_field.get()),str(self.qnt1_field.get())),
            (str(self.oc2_field.get()),str(self.qnt2_field.get())),
            (str(self.oc3_field.get()),str(self.qnt3_field.get())),
            (str(self.oc4_field.get()),str(self.qnt4_field.get())),
            (str(self.oc5_field.get()),str(self.qnt5_field.get())),
            (str(self.oc6_field.get()),str(self.qnt6_field.get())),
            (str(self.oc7_field.get()),str(self.qnt7_field.get())),
            (str(self.oc8_field.get()),str(self.qnt8_field.get())),
            (str(self.oc9_field.get()),str(self.qnt9_field.get())),
            (str(self.oc10_field.get()),str(self.qnt10_field.get())))

        if (self.numero_field.get() == "" and 
            self.cemb_field.get() == "" and
            self.qnt_field.get() == "" and
            self.oc1_field.get() == "" and
            self.oc2_field.get() == "" and
            self.oc3_field.get() == "" and
            self.oc4_field.get() == "" and
            self.oc5_field.get() == "" and
            self.oc6_field.get() == "" and
            self.oc7_field.get() == "" and
            self.oc8_field.get() == "" and
            self.oc9_field.get() == "" and
            self.oc10_field.get() == "" 
        ): messagebox.showinfo(message="Os campos estão vazios!")

        elif(self.oc1_field.get() == "" and
            self.oc2_field.get() == "" and
            self.oc3_field.get() == "" and
            self.oc4_field.get() == "" and
            self.oc5_field.get() == "" and
            self.oc6_field.get() == "" and
            self.oc7_field.get() == "" and
            self.oc8_field.get() == "" and
            self.oc9_field.get() == "" and
            self.oc10_field.get() == "" 
        ): messagebox.showinfo(message="Os campos de OC estão vazios!")

        else: 
            x = messagebox.askquestion(title="Double-Check", message="Confirma os dados do Form_173?")
            if x == "yes":
                try:
                    cursor.execute(    ### Inserindo dados na tabela
                        f"""INSERT INTO form_173 (solicitante, formulario, data_solicitacao, cemb, quantidade, pintor)
                        VALUES (?,?,?,?,?,?)
                        """,(dic[0], dic[1], dic[2], dic[3], dic[4], dic[5]))
                    cursor.execute("""SELECT rowid FROM form_173 WHERE rowid=(SELECT MAX(rowid) FROM form_173)""")
                    id_form173 = cursor.fetchone()[0] #Retorna o ID da última linha
                    banco.commit()
                except Exception as ex: messagebox.showerror(message=(ex, type(ex)))

                for i in dic_oc:
                    if not i[0] == "":
                        try:
                            text = """INSERT INTO ocs (oc, quantidade,track_form173) VALUES (?,?,?)"""
                            cursor.execute(text, [i[0], i[1], id_form173])
                            banco.commit()
                        except Exception as ex: messagebox.showerror(message=(ex, type(ex)))
                
                self.numero_field.focus_set()
                self.numero_field.delete(0, END)
                self.pintor_field.delete(0, END)
                self.cemb_field.delete(0, END)
                self.qnt_field.delete(0, END)
                self.oc1_field.focus_set() 
                self.oc1_field.delete(0, END)
                self.oc2_field.delete(0, END) 
                self.oc3_field.delete(0, END) 
                self.oc4_field.delete(0, END) 
                self.oc5_field.delete(0, END) 
                self.oc6_field.delete(0, END) 
                self.oc7_field.delete(0, END) 
                self.oc8_field.delete(0, END) 
                self.oc9_field.delete(0, END) 
                self.oc10_field.delete(0, END)
                self.qnt1_field.delete(0, END)
                self.qnt2_field.delete(0, END)
                self.qnt3_field.delete(0, END)
                self.qnt4_field.delete(0, END)
                self.qnt5_field.delete(0, END)
                self.qnt6_field.delete(0, END)
                self.qnt7_field.delete(0, END)
                self.qnt8_field.delete(0, END)
                self.qnt9_field.delete(0, END)
                self.qnt10_field.delete(0, END)
                self.numero_field.focus_set()  
                self.destroy()
            else: self.numero_field.focus_set()

    def limpar(self):
        self.numero_field.focus_set()
        self.numero_field.delete(0, END)
        self.pintor_field.delete(0, END)
        self.cemb_field.delete(0, END)
        self.qnt_field.delete(0, END)
        self.oc1_field.focus_set() 
        self.oc1_field.delete(0, END)
        self.oc2_field.delete(0, END) 
        self.oc3_field.delete(0, END) 
        self.oc4_field.delete(0, END) 
        self.oc5_field.delete(0, END) 
        self.oc6_field.delete(0, END) 
        self.oc7_field.delete(0, END) 
        self.oc8_field.delete(0, END) 
        self.oc9_field.delete(0, END) 
        self.oc10_field.delete(0, END)
        self.numero_field.focus_set()

# if __name__ == "__main__":
#     app = App()
#     app.mainloop()
# App()