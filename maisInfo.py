from tkinter import *
from tkinter import messagebox, ttk
import tkinter as tk
from DBfuncs import DBForm_173
from ttkbootstrap import Style as BsStyle
import tkinter.font as font
import re
from OC_ex import OC_ex


class MaisInfo(Toplevel):
    janela_aberta = False
    def __init__(info):
        if not MaisInfo.janela_aberta:
            MaisInfo.janela_aberta = True
            super().__init__()
            info.protocol("WM_DELETE_WINDOW", lambda: info.on_closing())
            info.geometry("400x350")
            info.configure(background='#f0f5ff')
            info.iconbitmap(r'logo.ico')
            info.resizable(0,0)
            info.title('Adicionar OC após o Form 173')
            info.screen_width = info.winfo_screenheight()
            info.create_wigets()
        else: 
            x = messagebox.showerror(message="Janela já aberta!", icon='warning')
            if x == 'ok':
                MaisInfo.focus_force()
        
        
    def on_closing(info):
        MaisInfo.janela_aberta = False
        info.destroy()
        
    def create_wigets(info):
        titulo = ttk.Label(info, text="Caso deseja vizualizar formulários finalizados, selecione um dos botões abaixo.", style='TituloMenor.TLabel',
                           wraplength=300, background='#f0f5ff')
        titulo.pack(pady=20)
        
        # Botão de vizualização dos Form173 finalizados
        btn_infoForm173 = ttk.Button(info, text='Form173', style='Custom.TButton')
        btn_infoForm173.pack(pady=20, padx=(0,0))
        
        # Botão de vizualização dos Form40 finalizados
        btn_infoForm40 = ttk.Button(info, text='Form40', style='Custom.TButton')
        btn_infoForm40.pack(pady=20, padx=(0,0))
        
        # Botão de vizualização dos Form40 finalizados
        btn_infoForm161 = ttk.Button(info, text='Form161', style='Custom.TButton')
        btn_infoForm161.pack(pady=20, padx=(0,0))
        

# if __name__ == "__main__":
#     app = addOC_ex()
#     app.mainloop()

