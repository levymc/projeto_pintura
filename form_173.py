from tkinter import * 
from tkinter import messagebox, ttk
import hashlib, json, sqlite3, re
from PIL import ImageTk, Image 
from datetime import datetime
import tkinter.font as font
from ttkbootstrap import Style as BsStyle
from ttkbootstrap.constants import *
from ttkbootstrap.widgets import Frame



class App(Tk):
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
        self.selected_option = IntVar()
        
        self.style = BsStyle(theme='flatly')
        self.style.configure('FundoOC.TFrame', background='#041536')
        self.style.configure('Principal.TFrame',
                             background='#f0f5ff',
                             )            
        self.style.map('Custom.TButton', background=[('active', '#cbd8f2')], 
          foreground=[('active', 'black')],
          bordercolor=[('active', '#384a6e')]) ## O .map serve para configuração de estilos de estado (pressionado, ativo, ....)
        self.style.configure('Custom.TButton', background='#294c91',  #.configure serve para configurações de estilo no geral
                font=('Helvetica', 9, 'bold'),
                foreground='white',
                borderwidth=5,
                relief='solid',
                bordercolor='#cbd8f2')   
        self.style.map('Limpar.TButton', background=[('active', '#b3c9f5')], 
          foreground=[('active', 'white')])  
        self.style.configure('Limpar.TButton',
                            background='#cbd8f2',
                            foreground='black',
                            font=('Helvetica', 7, 'bold'),
                             )
        
        try:
            banco = sqlite3.connect(self.db)
            cursor = banco.cursor()
            cursor.execute(f"SELECT codigo FROM operadores WHERE usuario='{self.user}'")
            self.cod_operador = cursor.fetchall()[0][0]
            cursor.close()
            banco.close()
        except Exception as ex: messagebox.showerror(message=(ex, type(ex)))

        self.create_wigets()
        
    def validate_entry_text(self, text):
        if text.isdigit() or text == "":
            return True
        else:
            return False

    def create_wigets(self):
        # Form 173 - Campo Principal
        q1 = ttk.Frame(self, width = 700, height = 460, style='Principal.TFrame')#, background="#f0f5ff"
        q1.place(x=0,y=0)
        x = ttk.Label(q1, text="Form. 173 - Solicitação de Preparação de Tinta", font='Impact 16', foreground='black', background='#f0f5ff')
        x.place(x=20, y=10)
        img_frame = ttk.Label(q1,image=self.img, background='#f0f5ff')
        img_frame.place(x=0, y=399)
        solicitante = ttk.Label(q1, text="Solicitante\n(Requesting Person)", font='Helvetica 9 bold', background='#f0f5ff')
        solicitante.place(x=40, y=60)
        self.solicitante_field = ttk.Label(q1, text=self.user+" - "+str(self.cod_operador), font='Helvetica 9 bold', foreground='#011336', background='#f0f5ff')
        self.solicitante_field.place(x=190, y=60)
        numero = ttk.Label(q1, text="Formulário Nº\n(Form Nº)", font='Helvetica 9 bold', foreground='#011336', background='#f0f5ff')
        numero.place(x=40, y=120)
        self.numero_field = ttk.Entry(q1)
        self.numero_field.place(x=190, y=120, width=150, height=30)
        pintor = ttk.Label(q1, text="Código do Pintor\n(Painter)", font='Helvetica 10 bold', foreground='#011336', background='#f0f5ff')
        pintor.place(x=40, y=180)
        self.hoje = datetime.today().strftime('%d-%m-%Y')
        self.agora = datetime.today().strftime('%d-%m-%Y %H:%M')
        self.pintor_field = ttk.Entry(q1)
        validate_pintor = (self.pintor_field.register(self.validate_entry_text), '%P')
        self.pintor_field.config(validate='key', validatecommand=validate_pintor)
        self.pintor_field.place(x=190, y=180, width=150, height=30)
        cemb = ttk.Label(q1, text="CEMB Tinta\n(Paint CODE)", font='Helvetica 9 bold', foreground='#011336', background='#f0f5ff')
        cemb.place(x=40, y=240)
        
        self.cemb_field = ttk.Entry(q1) #, highlightthickness=1
        validate_cemb = (self.cemb_field.register(self.validate_entry_text), '%P')
        self.cemb_field.config(validate='key', validatecommand=validate_cemb)
        self.cemb_field.place(x=190, y=240, width=150, height=30)
        
        qnt = ttk.Label(q1, text="Quantidade Solicitada\n(Quantity Requested)", font='Helvetica 9 bold', foreground='#011336', background='#f0f5ff')
        qnt.place(x=40, y=300)
        self.qnt_field = ttk.Entry(q1)
        validate_qnt = (self.qnt_field.register(self.validate_entry_text), '%P')
        self.qnt_field.config(validate='key', validatecommand=validate_qnt)
        self.qnt_field.place(x=190, y=300, width=150, height=30)
        
        self.grama = Checkbutton(q1, text="grama", variable=self.selected_option, onvalue=1, offvalue=0)
        self.grama.configure(foreground='#011336', background='#f0f5ff')
        self.grama.place(x=345, y=290)
        self.mililitro = Checkbutton(q1, text="mililitro", variable=self.selected_option, onvalue=2, offvalue=0)
        self.mililitro.configure(foreground='#011336', background='#f0f5ff')
        self.mililitro.place(x=345, y=320)
        
        botao = ttk.Button(q1, text="Enviar Solicitação", style='Custom.TButton')
        botao.bind('<Button-1>', self.insert)
        botao.place(x=310, y=370,height=50)
        limpar = ttk.Button(q1, text="Limpar Dados", command=self.limpar, style='Limpar.TButton')
        limpar.place(x=35, y=360,height=30)

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
                    self.oc_campo.focus_set()
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
        quadro = Frame(self, width = 250, height = 460, style='FundoOC.TFrame')#,bg="#041536"
        quadro.pack(side=RIGHT)
        
        add_oc = ttk.Label(quadro, text=f"OC: ", foreground='white', background="#041536", font='Helvetica 9 bold')
        add_oc.place(x=10, y=55)
        qnt = ttk.Label(quadro, text="Qnt.: ", foreground='white', background="#041536", font='Helvetica 9 bold')
        qnt.place(x=186, y=55)
        self.oc_campo = ttk.Entry(quadro, validate='key')
        validate_cmd = (self.oc_campo.register(self.validate_entry_text), '%P')
        self.oc_campo.config(validate='key', validatecommand=validate_cmd)
        self.oc_campo.place(x=45, y=55, height=20)
        self.qnt_campo = ttk.Entry(quadro)
        validate_qntOC = (self.qnt_campo.register(self.validate_entry_text), '%P')
        self.qnt_campo.config(validate='key', validatecommand=validate_qntOC)
        self.qnt_campo.place(x=220, y=55, width=20, height=20)    
        buttonAddOC = ttk.Button (quadro, text="Adicionar OC", command=campo_oc, style='Limpar.TButton')
        buttonAddOC.place(y=90, x=160, width=84, height=25)

        y = ttk.Label(quadro, text = "OC's utilizadas no lote: ",foreground='white', background="#041536", font='Impact 15')
        y.place(x=30, y=10)
        
        def atualizar_contador():
            infoOC.config(text=f"{self.mylistbox.size()} OC's adicionadas", foreground='white', background="#041536", font='Helvetica 9 bold')

        self.mylistbox=Listbox(quadro,width=35,height=6,  font='Trebuchet 9 bold', bg='white', selectmode=SINGLE)
        self.mylistbox.place(x=35,y=150, width=190, height=250)
        infoOC = ttk.Label(quadro, text=f"{self.mylistbox.size()} OC's adicionadas", foreground='white', background="#041536", font='Helvetica 9 bold')
        infoOC.place(x=33, y=405)
        deletarOC = Button(quadro, font=self.fonte_fa, text=u"\uf1f8", anchor='center', command=deletar_oc,  bg='red', fg='black')
        deletarOC.place(x=200, y=405)

        self.mainloop()

    def select_grama(self):
        self.mililitro.deselect()
        
    def select_mililitro(self):
        self.grama.deselect()

    def insert(self, event): 
        unidade = 'ml' if self.selected_option.get() == 2 else 'g'
        unidade = '' if self.selected_option.get() == 0 else unidade
        dic = (self.cod_operador, self.numero_field.get(), self.hoje, self.cemb_field.get(), self.qnt_field.get(), unidade,self.pintor_field.get())
        
        ### CONFERINDO OS CAMPOS VAZIOS
        if (self.numero_field.get() == "" or 
            self.cemb_field.get() == "" or
            self.qnt_field.get() == "" or
            unidade == "" or
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
                        f"""INSERT INTO form_173 (solicitante, formulario, data_solicitacao, cemb, quantidade, unidade, pintor)
                        VALUES (?,?,?,?,?,?,?)
                        """,(dic[0], dic[1], dic[2], dic[3], dic[4], dic[5], dic[6]))
                    banco.commit()
                    id_form173 = cursor.lastrowid
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
                self.selected_option.set(0)
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

if __name__ == "__main__":
    app = App('levymc', r"pintura.db")
    app.mainloop()
# App('teste')