from tkinter import *
from tkinter import messagebox, ttk
import tkinter as tk
from DBfuncs import conteudoForm173_pendente
import tkinter.font as font
import re


class OC_ex(Toplevel):
    def __init__(self, id_form173):
        super().__init__()
        self.geometry("250x460")
        self.configure(background='#041536')
        self.iconbitmap(r'logo.ico')
        self.resizable(0,0)
        self.title('Adicionar OC após o Form 173')
        self.screen_width = self.winfo_screenheight()
        self.fonte_fa = font.Font(family="FontAwesome", size=9)
        self.numero_ocs = 0
        self.y = 50
        self.ocs = []
        self.ocsAux = {}
        self.id_form173 = id_form173
        self.create_wigets()
        
    def validate_entry_text(self, text):
        if text.isdigit() or text == "":
            return True
        else:
            return False
        
    def create_wigets(self):
        print(self.id_form173)
        add_oc = Label(self, text=f"OC: ", foreground='white', background="#041536", font='Helvetica 9 bold')
        add_oc.place(x=10, y=55)
        qnt = Label(self, text="Qnt.: ", foreground='white', background="#041536", font='Helvetica 9 bold')
        qnt.place(x=186, y=55)
        self.oc_campo = Entry(self, highlightthickness=1, validate='key')
        validate_cmd = (self.oc_campo.register(self.validate_entry_text), '%P')
        self.oc_campo.config(validate='key', validatecommand=validate_cmd)
        self.oc_campo.place(x=55, y=55)
        self.qnt_campo = Entry(self, highlightthickness=1)
        validate_qntOC = (self.qnt_campo.register(self.validate_entry_text), '%P')
        self.qnt_campo.config(validate='key', validatecommand=validate_qntOC)
        self.qnt_campo.place(x=220, y=55, width=20)    
        buttonAddOC = Button (self, font='Helvetica 8 bold', text="Adicionar OC", anchor='center', command=self.campo_oc,  bg='#99d199')
        buttonAddOC.place(y=90, x=160, width=80, height=22)

        y = Label(self, text = "Adicionar OC: ",foreground='white', background="#041536", font='Impact 15')
        y.place(x=30, y=10)
        
        self.mylistbox=Listbox(self,width=35,height=6,  font='Trebuchet 9 bold', bg='white', selectmode=SINGLE)
        self.mylistbox.place(x=35,y=150, width=190, height=250)
        self.infoOC = Label(self, text=f"{self.mylistbox.size()} OC's adicionadas", foreground='white', background="#041536", font='Helvetica 9 bold')
        self.infoOC.place(x=33, y=405)
        deletarOC = Button(self, font=self.fonte_fa, text=u"\uf1f8", anchor='center', command=self.deletar_oc,  bg='red', fg='black')
        deletarOC.place(x=200, y=405)
        OC_ex.mainloop(self)
    
    def atualizar_contador(self):
        self.infoOC.config(text=f"{self.mylistbox.size()} OC's adicionadas", foreground='white', background="#041536", font='Helvetica 9 bold')
        
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
    
    
    
# if __name__ == "__main__":
#     app = addOC_ex()
#     app.mainloop()

