from tkinter import *
from tkinter import messagebox
import hashlib, json, sqlite3, form_40, login_40

def pend():
    try:
        banco = sqlite3.connect(r'pintura.db')
        cursor = banco.cursor()
    except Exception as ex: messagebox.showerror(message=[ex, type(ex)])
    cursor.execute("SELECT * FROM form_173 WHERE pendencia=1")
    valor = cursor.fetchall()
    cursor.close()
    banco.close()
    return valor

def tamanho():
    try:
        banco = sqlite3.connect(r'pintura.db')
        cursor = banco.cursor()
    except Exception as ex: messagebox.showerror(message=[ex, type(ex)])
    cursor.execute("SELECT * FROM form_173")
    tudo = cursor.fetchall()
    tamanho = len(tudo)
    cursor.close()
    banco.close()
    return tudo, tamanho

class Pendencias(Toplevel):
    def __init__(self):
        super().__init__()
        self.geometry("640x300")
        self.configure(background='#f0f5ff')
        self.iconbitmap(r'logo.ico')
        self.resizable(0,0)
        self.title('Solicitações Pendentes')
        self.screen_width = self.winfo_screenheight()
        self.create_wigets()
    
    def create_wigets(self):
        pendencias = pend()
        valor = len(pendencias)
        q = Frame(self, width = self.screen_width, height = 60, background='#041536')
        q.place(x=0)
        self.label_ = Label(self,  text=f'{valor}  Solicitações Pendentes', font='Impact 24 ', bg='#041536', foreground='white')
        self.label_.place(x=170, y=14)
        x=20
        y=100
        
        for i in range(valor):
            ids = pend()
            id_form173,solicitantes,formulario,data,cemb,qnt,p,pintor = ids[i]
            b = Button(self, text=f"Formulário: {formulario}", border=5,  font='Trebuchet 11 bold', bg='#d1d6e0', activebackground='#b4b5b8', command=lambda i=i:abrir(i))
            b.place(x=x, y=y, width=110, height=40)
            if i<=3:
                x+=160
                y=100
            if i==3:
                x = 20
                y = 180
            if i>3:
                x += 160
                y = 180
            if i>8:
                x = 9999
                y = 9999

            def abrir(i):
                self.destroy()
                try:
                    banco = sqlite3.connect(r'pintura.db')
                    cursor = banco.cursor()
                except Exception as ex: messagebox.showerror(message=[ex, type(ex)])
                id_form173,solicitantes,formulario,data,cemb,qnt,p,pintor = ids[i]
                ocs = [()]
                oc_ = cursor.execute(f"SELECT oc FROM ocs WHERE track_form173 = '{id_form173}'").fetchall()
                ocs.append((id_form173, oc_))
                cursor.close()
                banco.close()
                try:
                    pend_2 = Toplevel()
                    pend_2.geometry("886x300")
                    pend_2.iconbitmap(r'logo.ico')
                    loadimage_form173_2 = PhotoImage(file=r"form_173.png")
                    pend_2.configure(background='white')
                    pend_2.resizable(0,0)
                    
                    img_frame_173_2 = Label(pend_2, image=loadimage_form173_2, background='white')
                    img_frame_173_2.place(x=0,y=0)


                    solicitante = Label(pend_2, text = f"{solicitantes}", bg='white', font='Trebuchet 16 bold')
                    solicitante.place(x=210, y=105)

                    form = Label(pend_2, text = f"{formulario}", bg='white', font='Trebuchet 16 bold')
                    form.place(x=220, y=160)

                    data = Label(pend_2, text = ""+ f"{data}", bg='white', font='Trebuchet 16 bold')
                    data.place(x=680, y=102)

                    cembs = Label(pend_2, text ="E"+f"{cemb}", bg='white', font='Trebuchet 16 bold')
                    cembs.place(x=590, y=160)

                    quantidades = Label(pend_2, text = f"{qnt}", bg='white', font='Trebuchet 16 bold')
                    quantidades.place(x=300, y=220)

                    form_40_button = Button(pend_2, text='Formulário 40', border=5,  font='Trebuchet 14 bold', bg='#c3cdde', activebackground='#b4b5b8', command=lambda:login_40.Login(id_form173))
                    form_40_button.place(x=700, y=225)

                    finalizar_message = Label(pend_2, text='<-- Ao terminar de enviar o Formulário 40, finalize esta pendência!!!', fg='#940000',  font='Trebuchet 10 bold')
                    finalizar_message.place(x=75, y=265)
                    finalizar_button = Button(pend_2, text='Finalizar', border=5,  font='Trebuchet 8 bold', foreground='black', bg='#f26f6f', activebackground='#b4b5b8', command=lambda:self.finalizar(id_form173, pend_2))
                    finalizar_button.place(x=10, y=260)
                    pend_2.mainloop()

                except: 
                    pend_2.destroy()
                    messagebox.showinfo(message="Solicitação não encontrada!")
                    
      
        self.mainloop()
        banco.commit()
    
    def atualizar(self):
        valor = len(pend())
        self.label_.config(text=f"{valor}  Solicitações Pendentes")
        # print(valor)

    def finalizar(self,id_form173, pend_2):
        try:
            banco = sqlite3.connect(r'pintura.db')
            cursor = banco.cursor()
        except Exception as ex: messagebox.showerror(message=[ex, type(ex)])
        x = messagebox.askquestion(message="Deve finalizar?")
        if x =='yes':
            pend_2.destroy()
            cursor.execute(f"UPDATE form_173 SET pendencia={0} WHERE Id_form_173={id_form173}")
            banco.commit()
            cursor.close()
            banco.close()
        else: pass

def conteudo_form40():
    try:
        banco = sqlite3.connect(r'pintura.db')
        cursor = banco.cursor()
    except Exception as ex: messagebox.showerror(message=[ex, type(ex)])
    tudo = cursor.execute("SELECT * FROM form_40")
    conteudo = tudo.fetchall()
    tamanho = len(tudo)
    cursor.close()
    banco.close()
    return conteudo, tamanho



# if __name__ == "__main__":
#     app = Form_40()
#     app.mainloop()

