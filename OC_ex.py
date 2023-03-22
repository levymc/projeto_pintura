from tkinter import *
from tkinter import messagebox, ttk
import tkinter as tk
from DBfuncs import OCs, DBForm_40
from ttkbootstrap import Style as BsStyle
import tkinter.font as font
import re


class OC_ex(Toplevel):
    janela_aberta = False
    def __init__(self, dados, db):
        if not OC_ex.janela_aberta:
            OC_ex.janela_aberta = True
            super().__init__()
            self.geometry("600x480")
            self.configure(background='#f0f5ff')
            self.iconbitmap(r'logo.ico')
            self.protocol("WM_DELETE_WINDOW", lambda: self.on_closing())
            self.resizable(0,0)
            self.titulo = 'Configurar OCs do Formulário '+ str(dados['formulario'])
            self.title(self.titulo)
            self.screen_width = self.winfo_screenheight()
            self.numero_ocs = 0
            self.y = 50
            self.ocs = []
            self.ocsAux = {}
            self.id_form173 = dados['Id_form173']
            print(dados)
            self.dados = dados
            self.db = db
            self.create_wigets()
        else: 
            messagebox.showerror(message="Janela já aberta!", icon='warning')
            self.focus()
        
    def on_closing(self):
        OC_ex.janela_aberta = False
        self.destroy()
        
    def validate_entry_text(self, text):
        if text.isdigit() or text == "":
            return True
        else:
            return False
        
    def create_wigets(self):
        quadro = ttk.Frame(self, width = 255, height = 480, style='FundoOC.TFrame')#,bg="#041536"
        quadro.pack(side=RIGHT)
        
        add_oc = ttk.Label(quadro, text=f"OC: ", foreground='#f0f5ff', background="#203C75", font='Roboto 9 bold')
        add_oc.place(x=10, y=40)
        qnt = ttk.Label(quadro, text="Qnt.: ", foreground='#f0f5ff', background="#203C75", font='Roboto 9 bold')
        qnt.place(x=170, y=40)
        self.oc_campo = ttk.Entry(quadro, validate='key')
        validate_cmd = (self.oc_campo.register(self.validate_entry_text), '%P')
        self.oc_campo.config(validate='key', validatecommand=validate_cmd)
        self.oc_campo.place(x=45, y=35, width=120)
        self.qnt_campo = ttk.Entry(quadro)
        validate_qntOC = (self.qnt_campo.register(self.validate_entry_text), '%P')
        self.qnt_campo.config(validate='key', validatecommand=validate_qntOC)
        self.qnt_campo.place(x=204, y=35, width=30)    
        buttonAddOC = ttk.Button (quadro, text="Adicionar OC", command=lambda:[self.campo_oc()], style='Limpar.TButton')
        buttonAddOC.place(y=80, x=150, width=84, height=25)

        # y = ttk.Label(quadro, text = "OC's utilizadas no lote: ",foreground='#f0f5ff', background="#203C75", font='Impact 14')
        # y.place(x=40, y=10)

        self.mylistbox=Listbox(quadro,width=35,height=6,  font='Trebuchet 9 bold', bg='white', selectmode=SINGLE)
        self.mylistbox.place(x=42,y=130, width=190, height=250)
        self.infoOC = ttk.Label(quadro, text=f"{self.mylistbox.size()} OC's adicionadas", foreground='white', background="#203C75", font='Roboto 9 bold')
        self.infoOC.place(x=40, y=395)
        deletarOC = ttk.Button(quadro, style='Deletar.TButton', text=u"Deletar", command=lambda:[self.deletar_oc()])
        deletarOC.place(x=181, y=395)
        botao = ttk.Button(quadro, text="Adicionar OCs", style='Enviar2.TButton', command=lambda:self.insert())
        botao.place(x=135, y=440,height=30)
        
        # Lado "Remove" OCs
        
        self.titleBody = ttk.Label(self, text=self.titulo, background='#f0f5ff', font='Roboto 14 bold',foreground='#203C75')
        self.titleBody.pack(pady=(10,0))
        
        self.tableRemove = ttk.Treeview(self, columns=('Id_ocs', 'n°', 'OC', 'Quantidade'), style='RemoveOC.Treeview')
        self.tableRemove.configure(height=10)
        self.tableRemove.column('#0',width=0, minwidth=0)
        self.tableRemove.column('#1',width=0, minwidth=0)
        self.tableRemove.column('#2',width=80, anchor=tk.CENTER)
        self.tableRemove.column('#3',width=80, anchor=tk.CENTER)
        self.tableRemove.column('#4',width=80, anchor=tk.CENTER)
        
        # Adiciona as colunas à tabela
        self.tableRemove.heading('#0', text='ID')
        self.tableRemove.heading('#1', text='Id_ocs')
        self.tableRemove.heading('#2', text='n°')
        self.tableRemove.heading('#3', text='OC')
        self.tableRemove.heading('#4', text='Quantidade')
        
        # Define o Scrollbar e o adiciona ao Frame
        solicit_scroll = ttk.Scrollbar(self, orient='vertical', command=self.tableRemove.yview)
        solicit_scroll.pack(side='right', ipady=155, pady=(0,45),padx=(0, 20))
        
        #Adicionando linhas na tabela
        for i in range(len(OCs.consultaEspecifica(self.id_form173, 'track_form173'))):
            self.tableRemove.insert('', 'end', text='1', values=(OCs.consultaEspecifica(self.id_form173, 'track_form173')[i]['Id_ocs'] ,i+1, OCs.consultaEspecifica(self.id_form173, 'track_form173')[i]['oc'], OCs.consultaEspecifica(self.id_form173, 'track_form173')[i]['quantidade']))
        self.tableRemove.pack(padx=(10,2), pady=(25,15))
        self.tableRemove.configure(yscrollcommand=solicit_scroll.set)
        
        # solicit_scroll.config())  # Define a altura do Scrollbar com base no número de linhas exibidas no Treeview
        
        btn_deletar = ttk.Button(self, text='Deletar OC', command=lambda:self.carrega_linha_selecionada(), style='ApagarOCexcessao.TButton')
        btn_deletar.pack(pady=10, padx=(0, 0), ipady=4, side='bottom')
        
        # Cria uma variável para armazenar as informações da linha selecionada
        self.linha_selecionada = {}

        OC_ex.mainloop(self)
        
    def carrega_linha_selecionada(self): # Obtém o ID da linha selecionada
        if not self.tableRemove.selection():
            messagebox.showinfo(message="Selecione uma OC.")
            self.focus()
        else:
            id_linha = self.tableRemove.selection()[0] # Obtém as informações da linha selecionada
            info_linha = self.tableRemove.item(id_linha)['values'] # Armazena as informações na variável linha_selecionada
            self.linha_selecionada = {
                'Id_ocs': info_linha[0],
                'n': info_linha[1],
                'oc': info_linha[2],
                'quantidade': info_linha[3],
            }
            self.removerOC_DB()
    
    
    def removerOC_DB(self):
        resposta = messagebox.askquestion("Remover OC", "Deseja remover esta OC do Formulário?")
        if resposta == 'yes':
            
            id_linha = self.tableRemove.selection()[0] # Obtém as informações da linha selecionada
            info_linha = self.tableRemove.item(id_linha)['values'] # Armazena as informações na variável linha_selecionada
            self.linha_selecionada = {
                'Id_ocs': info_linha[0],
                'n': info_linha[1],
                'oc': info_linha[2],
                'quantidade': info_linha[3],
            }
            print("Removendo a linha: ", self.linha_selecionada)
            
            ## Removendo OC da Tabela e do DB e depois retornando a janela
            print(type(info_linha[0]))
            OCs.removeOC(info_linha[0])
            self.tableRemove.delete(id_linha)
            try:
                DBForm_40.update_print(self.id_form173)
            except Exception as ex:
                messagebox.showerror("Error", ex)
                print(ex, type(ex))
            self.focus()
            
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
            x = messagebox.askquestion(title="Double-Check", message="Confirma a adição de OCs?")
            if x == "yes":
                for i in range(len(self.ocs)):
                    items = self.tableRemove.get_children()
                    last_item = items[-1] 
                    self.tableRemove.insert('', 'end', text='1', values=(self.tableRemove.item(last_item)['values'][0]+1 ,
                                            self.tableRemove.item(last_item)['values'][1]+1, 
                                            self.ocs[i]['oc'], 
                                            self.ocs[i]['qnt'])
                                            )
                    # self.tableRemove.insert('', 'end', text='1', values=(9, oc['oc'], self.id_form173, 40))
                OCs.insertOC(self.id_form173, self.ocs)
                print(self.id_form173)
                try:
                    DBForm_40.update_print(self.id_form173)
                except Exception as ex:
                    messagebox.showerror("Error", ex)
                    print(ex, type(ex))
                self.ocs = []
                
                # APAGANDO OS CAMPOS APÓS O ENVIO DAS INFO..
                self.oc_campo.delete(0, END)
                self.qnt_campo.delete(0, END)
                self.mylistbox.delete(0, END)
                self.atualizar_contador()
                self.focus()
                
            else: self.oc_campo.focus_set()
    
# if __name__ == "__main__":
#     app = OC_ex(1)
#     app.mainloop()
