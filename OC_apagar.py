from tkinter import *
from tkinter import messagebox, ttk
import tkinter as tk
from DBfuncs import conteudoForm173_pendente, insertOC
from ttkbootstrap import Style as BsStyle
import tkinter.font as font
import re


class OC_apagar(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("350x480")
        self.configure(background='#f0f5ff')
        self.iconbitmap(r'logo.ico')
        self.resizable(0,0)
        self.title('Adicionar OC após o Form 173')
        self.screen_width = self.winfo_screenheight()
        # self.id_form173 = dados['Id_form173']
        # self.dados = dados
        
        self.create_wigets()
        
    def create_wigets(self):
        titulo = ttk.Label(self, text="")
        titulo.pack(pady=20)
        
        self.mainloop()
        
if __name__ == "__main__":
    app = OC_apagar()
    app.mainloop()