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
from maisInfo import MaisInfo
import local
from DBfuncs import DBForm_173, Operadores

db = local.Local.local()

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
        self.bind("<Button-3>", lambda event: self.exibir_menu(event))
        
        self.create_wigets()

    def exibir_menu(self, event):
        menu = Menu(self, tearoff=0)
        menu.add_command(label="Opção 1", command=lambda:print("oiiiii!!"))
        menu.add_command(label="Opção 2")
        menu.add_separator()
        menu.add_command(label="Sair", command=lambda: self.quit())
        menu.post(event.x_root, event.y_root)
    
    def create_wigets(self):
        quadro0 = ttk.Frame(self, width= 683, height=80, style='Frame1.TFrame')
        quadro0.place(x=0, y=0)
        titulo = ttk.Label(quadro0,  font='Impact 35 bold', text=f"Processos Pintura", background='#041536', foreground='#f0f5ff')
        titulo.place(x =160 , y= 8)
        
        quadro = Frame(self, width= 683, height=320, style='TFrame')
        quadro.place(x=0, y=80)
        # processo = ttk.Button(quadro, text="Email Processo", style='Processo.TButton', command=lambda:[Interface()])
        # processo.place(x = 595, y=274)
        
        maisInfo = ttk.Button(quadro, text="Mais Informações", style="MaisInfo.TButton", command=lambda:MaisInfo())
        maisInfo.place(x = 565, y = 274)
        
        img_frame = ttk.Label(quadro,image=self.img, background='#f0f5ff')
        img_frame.place(x=0, y=240)

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
        
        atualizar_bt = ttk.Button(quadro, text="Atualizar",command=lambda:popular(), takefocus=False, style='Att.TButton')
        atualizar_bt.place(x=600, y=156)
        solicit = ttk.Label(quadro, text=f"Solicitações {self.hoje}: ",foreground='#041536', background='#f0f5ff',  font='Trebuchet 10 bold')
        solicit.place(x=460,y=15)
        solicit_scroll = Scrollbar(quadro, orient='vertical', background='white')
        solicit_scroll.place(x=400, y=40, height=90)
        legenda = ttk.Label(quadro, text="Id | Solicitante - Cód. | Formulário | CEMB | Quantidade | Pintor",foreground='#041536', background='#f0f5ff',  font='Trebuchet 6 bold')
        legenda.place(x=420, y= 138)

        mylistbox=Listbox(quadro,width=35,height=6,  font='Trebuchet 9 bold', background='white', selectmode=SINGLE)
        mylistbox.place(x=420,y=39)

        def popular():
            mylistbox.delete(0, END)
            dados = DBForm_173.conteudoTudoEspecificoDia()
            for i in dados:
                nome = Operadores.consultaEspecificaCodigo(i['solicitante'])[0]['nome']
                print(nome) 
                print(str(i['Id_form_173']))
                mylistbox.insert(END, str(i['Id_form_173']) + " | "+ nome +" | "+ str(i['solicitante']) +" | "+ str(i['formulario']) +" | "+ str(i['cemb']) +" | "+ str(i['quantidade']) +" | "+ str(i['pintor']))
        popular()
        solicit_scroll.config(command=mylistbox.yview)

        b1 = ttk.Button(quadro, text="Formulário 173 - Solicitações", command=lambda:[login_173.Login(db)], style='Custom.TButton', takefocus=False)
        b1.place(x = 50, y= 40)
        b2 = ttk.Button(quadro, text="Solicitações de Mescla Pendentes", command=lambda:[pend_new.Pendencias(db)], style='Custom.TButton', takefocus=False)
        b2.place(x = 50, y= 110)
        b3 = ttk.Button(quadro, text="Gerar e Imprimir Form. 161", command=lambda:[mesclas.Mesclas(db)], style='Custom.TButton', takefocus=False)
        b3.place(x = 50, y= 180)
        
if __name__ == "__main__":
    app = Main()
    app.mainloop()