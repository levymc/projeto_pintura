from tkinter import * 
from tkinter import messagebox, ttk
import hashlib, json, sqlite3
from PIL import ImageTk, Image 
import form_173, pend_new, form_40, login_173, mesclas, addOC_ex
from datetime import datetime
from ttkthemes import ThemedStyle

agora = datetime.today().strftime('%d.%m.%Y_%H.%M')
meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
anoAtual = agora[6:10]+"/"
mesAtual = meses[int(agora[3:5])-1]+"/"
dia_mesAtual = agora[:5]+"/"

local = "dev"

if local == "dev":
    db = r"pintura.db"
    path = r"./Forms/Form_161.xlsx"
    path_maior = r"./Forms/Form_161_maior.xlsx"
    path_gerado = r"./Forms/Form_161_Gerado/" + anoAtual + mesAtual + dia_mesAtual
elif local == "prod":
    db = r'//NasTecplas/Pintura/DB/pintura.db'
    path = r"//NasTecplas/Pintura/Forms/Form_161/Form_161.xlsx"
    path_maior = r"//NasTecplas/Pintura/Forms/Form_161/Form_161_maior.xlsx"
    path_gerado = r"//NasTecplas/Pintura/Forms/Form_161/Form_161_Gerado/"+anoAtual+mesAtual+dia_mesAtual

def pend():
    try:
        banco = sqlite3.connect(db)
        cursor = banco.cursor()
        cursor.execute("SELECT * FROM form_173 WHERE pendencia=1")
        valor = cursor.fetchall()
        cursor.close()
        banco.close()
        return valor
    except Exception as ex: messagebox.showerror(message=[ex, type(ex)])

def tamanho():
    try:
        banco = sqlite3.connect(db)
        cursor = banco.cursor()
        cursor.execute("SELECT * FROM form_173")
        tudo = cursor.fetchall()
        tamanho = len(tudo)
        cursor.close()
        banco.close()
        return tudo, tamanho
    except Exception as ex: messagebox.showerror(message=[ex, type(ex)])

class Main(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("683x384")
        self.configure(background='#041536')
        self.resizable(0,0)
        self.hoje = datetime.today().strftime('%d-%m-%Y')
        self.title('TECPLAS - Pintura (main)')
        self.iconbitmap(r'logo.ico')
        self.img = PhotoImage(file="logo.png")
        self.style = ThemedStyle()
        self.create_wigets()

    def create_wigets(self):
        try:
            banco = sqlite3.connect(db)
            cursor = banco.cursor()
            pendencias = pend()
            cursor.execute(f"SELECT * FROM form_173 WHERE pendencia={0}")
            n_pend = cursor.fetchall()[0][0]
            cursor.close()
            banco.close()
        except:pass
        titulo = Label(self,  font='Impact 35 bold', text=f"Processos Pintura",foreground='#f0f5ff', bg='#041536')
        titulo.place(x =160 , y= 8)
        quadro = Frame(self, width= 683, height=320, bg='#f0f5ff')
        quadro.place(x=0, y=80)
        img_frame = Label(quadro,image=self.img, background='#f0f5ff')
        img_frame.place(x=0, y=240)

        def proc_solicitacao(db):
            # x = consulta_field.get()
            try:
                banco = sqlite3.connect(db)
                cursor = banco.cursor()
                cursor.execute(f"SELECT * FROM form_173 WHERE Id_form_173={x[0]}")
                vetor_inform = cursor.fetchall()
                print(vetor_inform[0])
                id_form173,solicitantes,formulario,data,cemb,qnt,p,pintor = vetor_inform[0]
                cursor.close()
                banco.close()
            except:
                messagebox.showinfo(message="Solicitação não encontrada!")
            try:
                    pend_ = Toplevel()
                    pend_.geometry("886x300")
                    pend_.iconbitmap(r'logo.ico')
                    loadimage_form173 = PhotoImage(file=r"form_173.png")
                    pend_.configure(background='white')
                    pend_.resizable(0,0)
                    img_frame_173 = Label(pend_, image=loadimage_form173, background='#f0f5ff')
                    img_frame_173.place(x=0,y=0)
                    solicitante = Label(pend_, text = f"{solicitantes}", bg='white', font='Trebuchet 16 bold')
                    solicitante.place(x=210, y=105)
                    form = Label(pend_, text = f"{formulario}", bg='white', font='Trebuchet 16 bold')
                    form.place(x=220, y=160)
                    data = Label(pend_, text = ""+ f"{data}", bg='white', font='Trebuchet 16 bold')
                    data.place(x=680, y=102)
                    cembs = Label(pend_, text ="E"+f"{cemb}", bg='white', font='Trebuchet 16 bold')
                    cembs.place(x=590, y=160)
                    quantidades = Label(pend_, text = f"{qnt}", bg='white', font='Trebuchet 16 bold')
                    quantidades.place(x=300, y=220)

            except: 
                pend_.destroy()
                messagebox.showinfo(message="Solicitação não encontrada!")
                pass
            # consulta_field.delete(0, END)
            pend_.mainloop()


        self.style.set_theme("clearlooks")
        self.style.configure("TButton", padding=0, borderwidth=0, font='Roboto 8 bold', foreground="#3b0202")
        self.style.map("TButton", background=[("active", "#4CAF50")])
        self.style.map("TButton", background=[("disabled", "#f0f5ff")])

        # self.style.configure('Custom.TButton', 
        #         borderwidth=5,
        #         relief='groove',
        #         background='red', # cor de fundo
        #         foreground='white') #font='Trebuchet 11 bold',
        addOC_after = ttk.Button(quadro, text="Add OC a um Formulário",   style='TButton', command=lambda:[addOC_ex.addOC_ex()], takefocus=False)
        addOC_after.place(x=450, y=250)
        
        atualizar_bt = Button(quadro, text="Atualizar", bg='#d1d6e0', activebackground='#b4b5b8', command=lambda:popular(db))
        atualizar_bt.place(x=615, y=196)
        solicit = Label(quadro, text=f"Solicitações {self.hoje}: ",foreground='#041536', bg='#f0f5ff',  font='Trebuchet 12 bold')
        solicit.place(x=450,y=50)
        solicit_scroll = Scrollbar(quadro, orient='vertical', bg='white')
        solicit_scroll.place(x=400, y=80, height=90)
        legenda = Label(quadro, text="Id | Solicitante - Cód. | Formulário | CEMB | Quantidade | Pintor",foreground='#041536', bg='#f0f5ff',  font='Trebuchet 6 bold')
        legenda.place(x=420, y= 178)

        # def CurSelet(evt):
        #     try:
        #         value=str((mylistbox.get(mylistbox.curselection())))
        #         consulta_field.delete(0, END)
        #         consulta_field.insert(0, value)
        #     except:pass

        mylistbox=Listbox(quadro,width=35,height=6,  font='Trebuchet 9 bold', bg='white', selectmode=SINGLE)
        # mylistbox.bind('<<ListboxSelect>>',CurSelet)
        mylistbox.place(x=420,y=79)

        def popular(db):
            banco = sqlite3.connect(db)
            cursor = banco.cursor()
            mylistbox.delete(0, END)
            cursor.execute(f"SELECT Id_form_173, solicitante, formulario, cemb, quantidade, pintor FROM form_173 WHERE data_solicitacao='{self.hoje}'")
            dados_solicitacao = cursor.fetchall()
            for i in range(len(dados_solicitacao)):
                try:
                    cursor.execute(f"SELECT nome FROM operadores WHERE codigo = {dados_solicitacao[i][0]}")
                    nome = cursor.fetchall()
                    mylistbox.insert(END,str(dados_solicitacao[i][0])+" | "+ nome[0][0]+" - "+str(dados_solicitacao[i][1])+" | "+ str(dados_solicitacao[i][2])+" | "+ str(dados_solicitacao[i][3])+" | "+ str(dados_solicitacao[i][4])+" | "+ str(dados_solicitacao[i][5]))
                    cursor.close()
                    banco.close()
                except: 
                    mylistbox.insert(END,str(dados_solicitacao[i][0])+" | "+str(dados_solicitacao[i][1])+" | "+ str(dados_solicitacao[i][2])+" | "+ str(dados_solicitacao[i][3])+" | "+ str(dados_solicitacao[i][4])+" | "+ str(dados_solicitacao[i][5]))
        popular(db)
        solicit_scroll.config(command=mylistbox.yview)

        b1 = Button(quadro, text="Formulário 173 - Solicitações", border=5,  font='Trebuchet 11 bold', bg='#d1d6e0', activebackground='#b4b5b8', command=lambda:[login_173.Login(db)])
        b1.place(x = 50, y= 40)
        b2 = Button(quadro, text="Solicitações de Mescla Pendentes", border=5,  font='Trebuchet 11 bold', bg='#d1d6e0', activebackground='#b4b5b8', command=lambda:[pend_new.Pendencias(db)])
        b2.place(x = 50, y= 110)
        b3 = Button(quadro, text="Gerar e Imprimir Form. 161", border=5,  font='Trebuchet 11 bold', bg='#d1d6e0', activebackground='#b4b5b8', command=lambda:[mesclas.Mesclas(db,path, path_maior, path_gerado)])
        b3.place(x = 50, y= 180)
        

if __name__ == "__main__":
    app = Main()
    app.mainloop()

