from tkinter import *
from tkinter import messagebox
from datetime import datetime
import xlwings as xw
import hashlib, json, sqlite3, form_40, login_40, shutil, win32print, win32api

try:
    banco = sqlite3.connect(r'//NasTecplas/Public/Levy/dig_pintura/pintura.db')
    cursor = banco.cursor()
except Exception as ex: messagebox.showerror(message=[ex, type(ex)])
agora = datetime.today().strftime('%d-%m-%Y_%H.%M')
path = r"//NasTecplas/Public/Levy/dig_pintura/Form_161.xlsx"
new = r"//NasTecplas/Public/Levy/dig_pintura/"+agora+r".xlsx"

def tamanho():
    try:
        cursor.execute(f"SELECT * FROM form_40 WHERE print={0}")
        tudo = cursor.fetchall()
        tamanho = len(tudo)
        return tudo, tamanho
    except Exception as ex: messagebox.showerror(message=[ex, type(ex)])

class Mesclas(Toplevel):
    def __init__(self):
        super().__init__()
        self.geometry("640x300")
        self.configure(background='#f0f5ff')
        self.iconbitmap(r'logo.ico')
        self.resizable(0,0)
        self.title('Solicitações Pendentes')
        self.create_wigets()
    
    def create_wigets(self):
        tudo, valor = tamanho()
        q = Frame(self, width = 640, height = 60, background='#041536')
        q.place(x=0)
        self.label_ = Label(self,  text=f'{valor}  Mesclas Prontas', font='Impact 24 ', bg='#041536', foreground='white')
        self.label_.place(x=200, y=14)
        x=20
        y=100
        
        for i in range(valor):
            mescla_number = tudo[i][1]
            b = Button(self, text=f"Mescla: {mescla_number}", border=5,  font='Trebuchet 11 bold', bg='#d1d6e0', activebackground='#b4b5b8', command=lambda i=i:abrir(i))
            b.place(x=x, y=y, height=40, width=120)
            if i<=3:
                x+=180
                y=100
            if i==3:
                x = 20
                y = 180
            if i>3:
                x += 180
                y = 180
            if i>8:
                x = 9999
                y = 9999

            def abrir(i):
                try:
                    idform173 = tudo[i][22]
                    print(tudo[i][1])
                    cursor.execute(f"SELECT * FROM form_173 WHERE Id_form_173={idform173}")
                    form_173_tudo=cursor.fetchall()
                    x = messagebox.askquestion(message=f"Deseja imprimir o Fomulário 161 referente a mescla {tudo[i][1]}")
                    if x=='yes':
                        print(form_173_tudo, idform173)
                        shutil.copyfile(path, new)
                        try:
                            cursor.execute(f"SELECT * FROM ocs WHERE track_form173={form_173_tudo[0][0]}")
                            ocs = cursor.fetchall()
                            cursor.execute(f"SELECT nome FROM operadores WHERE codigo={form_173_tudo[0][1]}")
                            nome = cursor.fetchall()[0][0]
                            mescla_n = tudo[i][1]
                        except:messagebox.showinfo(message='Provavelmente o código do operador está errado!')

                        excel_app = xw.App(visible=False)
                        wb = excel_app.books.open(new)  # connect to an existing file in the current working directory
                        wks = xw.sheets
                        ws = wks[0]
                        linha = 35
                        for i in ocs:
                            ws.range("F"+f"{linha}").value = i[1]
                            ws.range("I"+f"{linha}").value = i[2]
                            linha += 1
                        ws.range("I4").value = datetime.today().strftime('%m-%d-%Y')
                        ws.range("C3").value = str(mescla_n).replace(",",".")
                        ws.range("C4").value = nome
                        ws.range("J3").value = form_173_tudo[0][4]
                        ws.range("K4").value = form_173_tudo[0][7]
                        wb.save()
                        wb.close()
                        excel_app.quit()

                        # lista_impressoras = win32print.EnumPrinters(2) #printar isso pra descobrir a impressora!
                        # impressora = lista_impressoras[3]
                        # win32print.SetDefaultPrinter(impressora[2]) # Coloca em Default a impressora a ser utilizada
                        # win32api.ShellExecute(0, "print", agora+r".xlsx", None, "//NasTecplas/Public/Levy/dig_pintura/", 0)

                        cursor.execute(f"UPDATE form_40 SET print={1} WHERE mescla='{mescla_n}'")
                        banco.commit()
                        print("IMPRIMIU!!!")
                        self.destroy()
                    else: 
                        self.mainloop()
                        pass
                except Exception as ex: messagebox.showerror(message=ex)

        self.mainloop()
        banco.commit()
    
    def atualizar(self):
        valor = len(pend())
        self.label_.config(text=f"{valor}  Solicitações Pendentes")
        # print(valor)

    def finalizar(self,id_form173):
        x = messagebox.askquestion(message="Deve finalizar?")
        if x =='yes':
            try:
                cursor.execute(f"UPDATE form_173 SET pendencia={0} WHERE Id_form_173={id_form173}")
            except Exception as ex: messagebox.showerror(message=ex)
        else: pass


# if __name__ == "__main__":
#     app = Mesclas()
#     app.mainloop()
#     banco.commit()
