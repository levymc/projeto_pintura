from tkinter import *
from tkinter import messagebox, ttk
import hashlib, json, sqlite3
import tkinter as tk
from DBfuncs import conteudoForm173_pendente

class addOC_ex(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("640x300")
        self.configure(background='#f0f5ff')
        self.iconbitmap(r'logo.ico')
        self.resizable(0,0)
        self.title('Adicionar OC após o Form 173')
        self.screen_width = self.winfo_screenheight()
        self.create_wigets()
        
    def create_wigets(self):
        teste = Label(self, text="  ")
        teste.pack()
        
        self.tree = ttk.Treeview(self, columns=('Solicitante', 'Formulário', 'Data', 'CEMB', 'Quantidade'))
        self.tree.column('#0',width=20)
        self.tree.column('#1',width=80, anchor=tk.CENTER)
        self.tree.column('#2',width=80, anchor=tk.CENTER)
        self.tree.column('#3',width=80, anchor=tk.CENTER)
        self.tree.column('#4',width=80, anchor=tk.CENTER)
        self.tree.column('#5',width=80, anchor=tk.CENTER)
        # Adiciona as colunas à tabela
        self.tree.heading('#0', text='ID')
        self.tree.heading('#1', text='Solicitante')
        self.tree.heading('#2', text='Formulário')
        self.tree.heading('#3', text='Data')
        self.tree.heading('#4', text='CEMB')
        self.tree.heading('#5', text='Quantidade')
        
        #Adicionando linhas na tabela
        for i in conteudoForm173_pendente():
            self.tree.insert('', 'end', text='1', values=(i[1], i[2], i[3], i[4], str(i[5])+i[6]))
        self.tree.pack()
        
        
        # self.mylistbox=Listbox(self,width=35,height=6,  font='Trebuchet 9 bold', bg='white', selectmode=SINGLE)
        # self.mylistbox.pack()
        
if __name__ == "__main__":
    app = addOC_ex()
    app.mainloop()

