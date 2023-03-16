from tkinter import * 
from tkinter import messagebox, ttk
import hashlib, json, sqlite3
from PIL import ImageTk, Image 
import form_173, pend_new, form_40, login_173, mesclas, addOC_ex
from datetime import datetime
from ttkbootstrap import Style as BsStyle
from ttkbootstrap.constants import *
from ttkbootstrap.widgets import Frame
import tkinter.font as font
from enviar_email import Interface
from style import Estilos

agora = datetime.today().strftime('%d.%m.%Y_%H.%M')
meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
anoAtual = agora[6:10]+"/"
mesAtual = meses[int(agora[3:5])-1]+"/"
dia_mesAtual = agora[:5]+"/"

local = "prod"

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
        self.resizable(0,0)
        self.hoje = datetime.today().strftime('%d-%m-%Y')
        self.title('TECPLAS - Pintura (main)')
        self.iconbitmap(r'logo.ico')
        self.img = PhotoImage(file="logo.png")
        self.fonte_fa = font.Font(family="FontAwesome", size=12)
        self.style = Estilos()
        
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
        
        quadro0 = ttk.Frame(self, width= 683, height=80, style='Frame1.TFrame')
        quadro0.place(x=0, y=0)
        titulo = ttk.Label(quadro0,  font='Impact 35 bold', text=f"Processos Pintura", background='#041536', foreground='#f0f5ff')
        titulo.place(x =160 , y= 8)
        
        
        quadro = Frame(self, width= 683, height=320, style='TFrame')
        quadro.place(x=0, y=80)
        processo = ttk.Button(quadro, text="Email Processo", style='Processo.TButton', command=lambda:[Interface()])
        processo.place(x = 595, y=274)
        
        
        img_frame = ttk.Label(quadro,image=self.img, background='#f0f5ff')
        img_frame.place(x=0, y=240)

        def proc_solicitacao(db):
            # x = consulta_field.get()
            try:
                banco = sqlite3.connect(db)
                cursor = banco.cursor()
                cursor.execute(f"SELECT * FROM form_173 WHERE Id_form_173={x[0]}")
                vetor_inform = cursor.fetchall()
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
                    img_frame_173 = ttk.Label(pend_, image=loadimage_form173, background='#f0f5ff')
                    img_frame_173.place(x=0,y=0)
                    solicitante = ttk.Label(pend_, text = f"{solicitantes}", background='white', font='Trebuchet 16 bold')
                    solicitante.place(x=210, y=105)
                    form = ttk.Label(pend_, text = f"{formulario}", background='white', font='Trebuchet 16 bold')
                    form.place(x=220, y=160)
                    data = ttk.Label(pend_, text = ""+ f"{data}", background='white', font='Trebuchet 16 bold')
                    data.place(x=680, y=102)
                    cembs = ttk.Label(pend_, text ="E"+f"{cemb}", background='white', font='Trebuchet 16 bold')
                    cembs.place(x=590, y=160)
                    quantidades = ttk.Label(pend_, text = f"{qnt}", background='white', font='Trebuchet 16 bold')
                    quantidades.place(x=300, y=220)

            except: 
                pend_.destroy()
                messagebox.showinfo(message="Solicitação não encontrada!")
                pass
            # consulta_field.delete(0, END)
            pend_.mainloop()

        frameOC = ttk.Frame(quadro, width=270, height=60, style='FrameOC.TFrame')
        frameOC.place(x=380, y=200)
        addOC_info = ttk.Label(quadro, style='infoOC.TLabel', text="Caso seja necessário corrigir as OCs\ncadastradas, clique ao lado")
        addOC_info.place(x=395, y=210)
        x = 0
        def clica(func,x):
            x += 1
            if not x > 1:
                func
            else: return True
        addOC_after = ttk.Button(quadro, padding=(3,3), text='Correção OCs',style='Add.TButton', bootstyle="outline", command=lambda:[clica(addOC_ex.addOC_ex(db), x)], takefocus=True)
        addOC_after.place(x=563, y=230)
        
        atualizar_bt = ttk.Button(quadro, text="Atualizar",command=lambda:popular(db), takefocus=False, style='Att.TButton')
        atualizar_bt.place(x=600, y=156)
        solicit = ttk.Label(quadro, text=f"Solicitações {self.hoje}: ",foreground='#041536', background='#f0f5ff',  font='Trebuchet 10 bold')
        solicit.place(x=460,y=15)
        solicit_scroll = Scrollbar(quadro, orient='vertical', background='white')
        solicit_scroll.place(x=400, y=40, height=90)
        legenda = ttk.Label(quadro, text="Id | Solicitante - Cód. | Formulário | CEMB | Quantidade | Pintor",foreground='#041536', background='#f0f5ff',  font='Trebuchet 6 bold')
        legenda.place(x=420, y= 138)

        mylistbox=Listbox(quadro,width=35,height=6,  font='Trebuchet 9 bold', background='white', selectmode=SINGLE)
        mylistbox.place(x=420,y=39)

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

        b1 = ttk.Button(quadro, text="Formulário 173 - Solicitações", command=lambda:[login_173.Login(db)], style='Custom.TButton', takefocus=False)
        b1.place(x = 50, y= 40)
        b2 = ttk.Button(quadro, text="Solicitações de Mescla Pendentes", command=lambda:[pend_new.Pendencias(db)], style='Custom.TButton', takefocus=False)
        b2.place(x = 50, y= 110)
        b3 = ttk.Button(quadro, text="Gerar e Imprimir Form. 161", command=lambda:[mesclas.Mesclas(db,path, path_maior, path_gerado)], style='Custom.TButton', takefocus=False)
        b3.place(x = 50, y= 180)
        

if __name__ == "__main__":
    app = Main()
    app.mainloop()

