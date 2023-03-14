from tkinter import *
from tkinter import messagebox, ttk
import tkinter as tk
from DBfuncs import conteudoForm173_pendente, insertOC
from ttkbootstrap import Style as BsStyle
import tkinter.font as font
import re


class OC_ex(Toplevel):
    def __init__(self, dados):
        super().__init__()
        self.geometry("250x480")
        self.configure(background='#041536')
        self.iconbitmap(r'logo.ico')
        self.resizable(0,0)
        self.title('Adicionar OC após o Form 173')
        self.screen_width = self.winfo_screenheight()
        self.numero_ocs = 0
        self.y = 50
        self.ocs = []
        self.ocsAux = {}
        self.id_form173 = dados['Id_form173']
        self.dados = dados
        print("ID: ", self.id_form173)
        
        self.style = BsStyle(theme='flatly')
        self.style.configure('FundoOC.TFrame', background='#203C75')
        self.style.configure('Principal.TFrame',
                             background='#f0f5ff',
                             )            
        self.style.map('Enviar2.TButton', background=[('active', '#a35c33')], 
          foreground=[('active', 'white')],
          bordercolor=[('active', '#384a6e')]) ## O .map serve para configuração de estilos de estado (pressionado, ativo, ....)
        self.style.configure('Enviar2.TButton', background='#f75c02',  #.configure serve para configurações de estilo no geral
                font=('Roboto', 8, 'bold'),
                foreground='white',
                borderwidth=0.3,
                relief='solid',
                border_radius=10,
                bordercolor='#cbd8f2')   
        self.style.map('Limpar.TButton', background=[('active', '#b3c9f5')], 
          foreground=[('active', 'white')])  
        self.style.configure('Limpar.TButton',
                            background='#cbd8f2',
                            foreground='black',
                            borderwidth=0.1,
                            font=('Roboto', 7, 'bold'),
                             )
        self.style.map('Deletar.TButton', background=[('active', '#f2bfbf')], 
          foreground=[('active', '#380101')])  
        self.style.configure('Deletar.TButton',
                            background='#a61919',
                            foreground='#f2bfbf',
                            borderwidth=0.3,
                            font=('Roboto', 7, 'bold'),
                             )
        
        self.create_wigets()
        
    def validate_entry_text(self, text):
        if text.isdigit() or text == "":
            return True
        else:
            return False
        
    def create_wigets(self):
        quadro = ttk.Frame(self, width = 255, height = 480, style='FundoOC.TFrame')#,bg="#041536"
        quadro.pack(side=RIGHT)
        
        add_oc = ttk.Label(quadro, text=f"OC: ", foreground='#f0f5ff', background="#203C75", font='Roboto 9 bold')
        add_oc.place(x=10, y=60)
        qnt = ttk.Label(quadro, text="Qnt.: ", foreground='#f0f5ff', background="#203C75", font='Roboto 9 bold')
        qnt.place(x=170, y=60)
        self.oc_campo = ttk.Entry(quadro, validate='key')
        validate_cmd = (self.oc_campo.register(self.validate_entry_text), '%P')
        self.oc_campo.config(validate='key', validatecommand=validate_cmd)
        self.oc_campo.place(x=45, y=55, width=120)
        self.qnt_campo = ttk.Entry(quadro)
        validate_qntOC = (self.qnt_campo.register(self.validate_entry_text), '%P')
        self.qnt_campo.config(validate='key', validatecommand=validate_qntOC)
        self.qnt_campo.place(x=204, y=55, width=30)    
        buttonAddOC = ttk.Button (quadro, text="Adicionar OC", command=lambda:[self.campo_oc()], style='Limpar.TButton')
        buttonAddOC.place(y=100, x=150, width=84, height=25)

        y = ttk.Label(quadro, text = "OC's utilizadas no lote: ",foreground='#f0f5ff', background="#203C75", font='Impact 14')
        y.place(x=40, y=10)

        self.mylistbox=Listbox(quadro,width=35,height=6,  font='Trebuchet 9 bold', bg='white', selectmode=SINGLE)
        self.mylistbox.place(x=42,y=150, width=190, height=250)
        self.infoOC = ttk.Label(quadro, text=f"{self.mylistbox.size()} OC's adicionadas", foreground='white', background="#203C75", font='Roboto 9 bold')
        self.infoOC.place(x=40, y=405)
        deletarOC = ttk.Button(quadro, style='Deletar.TButton', text=u"Deletar", command=lambda:[self.deletar_oc()])
        deletarOC.place(x=181, y=405)
        botao = ttk.Button(quadro, text="Enviar OCs", style='Enviar2.TButton', command=lambda:self.insert())
        botao.place(x=165, y=445,height=30)

        OC_ex.mainloop(self)
    
    def atualizar_contador(self):
        self.infoOC.config(text=f"{self.mylistbox.size()} OC's adicionadas", foreground='white', background="#203C75", font='Roboto 9 bold')
        
    def campo_oc(self):
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
                self.atualizar_contador()
    
    def deletar_oc(self):
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
        self.atualizar_contador()
    
    def insert(self): 
        if len(self.ocs) == 0: messagebox.showinfo(message="Os campos de OC's estão vazios!")
        else: 
            x = messagebox.askquestion(title="Double-Check", message="Confirma os dados do Form_173?")
            if x == "yes":
                insertOC(self.id_form173, self.ocs)
                messagebox.showinfo(message="Informações enviadas!!")
                self.ocs = []
                
                # APAGANDO OS CAMPOS APÓS O ENVIO DAS INFO..
                self.oc_campo.delete(0, END)
                self.qnt_campo.delete(0, END)
                self.mylistbox.delete(0, END)
            else: self.oc_campo.focus_set()
    
# if __name__ == "__main__":
#     app = OC_ex(1)
#     app.mainloop()
