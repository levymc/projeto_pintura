from tkinter import *
from tkinter import messagebox, ttk
import tkinter as tk
from DBfuncs import conteudoForm173_pendente
from OC_ex import OC_ex


class addOC_ex(Toplevel):
    janela_aberta = False
    def __init__(self):
        if not addOC_ex.janela_aberta:
            addOC_ex.janela_aberta = True
            super().__init__()
            self.protocol("WM_DELETE_WINDOW", lambda: self.on_closing())
            self.geometry("640x300")
            self.configure(background='#f0f5ff')
            self.iconbitmap(r'logo.ico')
            self.resizable(0,0)
            self.title('Adicionar OC após o Form 173')
            self.screen_width = self.winfo_screenheight()
            self.create_wigets()
        else: messagebox.showerror(message="Janela já aberta!", icon='warning')
        
        
    def on_closing(self):
        addOC_ex.janela_aberta = False
        self.destroy()
        
    def create_wigets(self):
        teste = Label(self, text="  ")
        teste.pack()
        
        self.tree = ttk.Treeview(self, columns=('id_form173', 'Formulário', 'Solicitante', 'Data', 'CEMB', 'Quantidade'))
        self.tree.column('#0',width=0, minwidth=0)
        self.tree.column('#1',width=0, minwidth=0)
        self.tree.column('#2',width=80, anchor=tk.CENTER)
        self.tree.column('#3',width=80, anchor=tk.CENTER)
        self.tree.column('#4',width=80, anchor=tk.CENTER)
        self.tree.column('#5',width=80, anchor=tk.CENTER)
        self.tree.column('#6',width=80, anchor=tk.CENTER)
        # self.tree.configure(displaycolumns=('#1'))
        # Adiciona as colunas à tabela
        self.tree.heading('#0', text='ID')
        self.tree.heading('#1', text='id_form173')
        self.tree.heading('#2', text='Formulário')
        self.tree.heading('#3', text='Solicitante')
        self.tree.heading('#4', text='Data')
        self.tree.heading('#5', text='CEMB')
        self.tree.heading('#6', text='Quantidade')
        
        #Adicionando linhas na tabela
        for i in conteudoForm173_pendente():
            self.tree.insert('', 'end', text='1', values=(i[0], i[2], i[1], i[3], i[4], str(i[5])+i[6]))
        self.tree.pack()
        
        # Cria uma variável para armazenar as informações da linha selecionada
        linha_selecionada = {}

        # Define uma função para o botão que carrega as informações da linha selecionada
        def carrega_linha_selecionada():
            # Obtém o ID da linha selecionada
            id_linha = self.tree.selection()[0]
            # Obtém as informações da linha selecionada
            info_linha = self.tree.item(id_linha)['values']
            # Armazena as informações na variável linha_selecionada
            linha_selecionada['Id_form173'] = info_linha[0]
            self.on_closing()
            if not addOC_ex.janela_aberta:
                OC_ex(info_linha[0])
            # Exibe as informações na tela
            self.destroy()
            print(linha_selecionada)

        # Cria o botão para carregar as informações da linha selecionada
        teste2 = Label(self, text="  ")
        teste2.pack()
        btn_carregar = tk.Button(self, text='Carregar linha selecionada', command=carrega_linha_selecionada)
        btn_carregar.pack()
        
        
# if __name__ == "__main__":
#     app = addOC_ex()
#     app.mainloop()

