from tkinter import *
from tkinter import messagebox, ttk
import tkinter as tk
from DBfuncs import conteudoForm173_pendente, insertOC
from ttkbootstrap import Style as BsStyle
import tkinter.font as font
import re


class OC_apagar(Toplevel):
    def __init__(self):
        super().__init__()
        self.geometry("350x480")
        self.configure(background='#041536')
        self.iconbitmap(r'logo.ico')
        self.resizable(0,0)
        self.title('Adicionar OC após o Form 173')
        self.screen_width = self.winfo_screenheight()
        # self.id_form173 = dados['Id_form173']
        # self.dados = dados
        
        self.create_wigets()
        
    def create_wigets(self):
        # fundo = ttk.Frame()
        titulo = ttk.Label(self, text=self.winfo_screenheight())
        titulo.pack()
        
        self.mainloop()
