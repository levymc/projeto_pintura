from tkinter import *
from tkinter import messagebox, ttk
from datetime import datetime
import xlwings as xw
import win32com.client as win32
import win32api
import sqlite3, shutil, win32print, re, pend_new, os, local
from DBfuncs import DBForm_40, DBForm_173, DBForm_161


nomeImp = local.Local.nomeImpressora()

def tamanho():
    try:
        tudo = DBForm_173.consultaEspecifica(0, 'print')
        tamanho = len(tudo)
        return tudo, tamanho
    except Exception as ex: messagebox.showerror(message=["mescla1",ex, type(ex)])

class Mesclas(Toplevel):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.path = local.Local.path()
        self.path_maior = local.Local.path_maior()
        self.path_gerado = local.Local.path_gerado()
        self.geometry("710x300")
        self.configure(background='#f0f5ff')
        self.iconbitmap(r'logo.ico')
        self.resizable(0,0)
        self.title('Formulário de Pintura')
        self.screen_width = self.winfo_screenheight()
        self.create_wigets()
    
    def create_wigets(self):
        tudo, valor = tamanho()
        q = ttk.Frame(self, width = self.screen_width, height = 60, style='Frame1.TFrame')
        q.place(x=0)
        self.label_ = ttk.Label(self,  text=f'{valor}  Formulários', font='Impact 24 ', background='#041536', foreground='white')
        self.label_.place(x=250, y=14)
        x=20
        y=100
        listaIds = []
        
        for i in range(valor):
            idform173 = tudo[i]['Id_form_173']
            listaIds.append(idform173)
            b = ttk.Button(self, text=f"CEMB: {DBForm_173.consultaEspecifica(idform173, 'Id_form_173')[0]['cemb']} - {i+1}", style='Mescla.TButton', command=lambda i=i:abrir(i))
            b.place(x=x, y=y)
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
                # print(listaIds[i])
                agora = datetime.today().strftime('%d.%m.%Y_%H.%M')
                try:
                    banco = sqlite3.connect(self.db)
                    cursor = banco.cursor()
                except Exception as ex: messagebox.showerror(message=["mescla2", ex, type(ex)])
                try:
                    #form_173_tudo = cursor.execute(f"SELECT * FROM form_173 WHERE Id_form_173={idform173}").fetchall()
                    form_173_tudo = DBForm_173.consultaEspecifica(listaIds[i], 'Id_form_173')
                    print(form_173_tudo)
                    x = messagebox.askquestion(message=f"Deseja imprimir o Fomulário 161 referente ao cemb CEMB: {DBForm_173.consultaEspecifica(idform173, 'Id_form_173')[0]['cemb']} - {i+1}")
                    if x=='yes':
                        try:
                            ocs = cursor.execute(f"SELECT * FROM ocs WHERE track_form173={idform173}").fetchall()
                            nome = cursor.execute(f"SELECT nome FROM operadores WHERE codigo={form_173_tudo[0]['solicitante']}").fetchall()[0]
                            contador = 1
                            # mescla_n = tudo[i]['mescla']
                        
                            if not os.path.exists(self.path_gerado):
                                os.makedirs(self.path_gerado)
                                print("CRIANDO O DIR: ",self.path_gerado)
                                if os.listdir(self.path_gerado) == []:
                                    new = self.path_gerado + "3- Form_Controle Aplicação Tinta "+ form_173_tudo[0]['cemb'] +" - "+ str(contador) + r".xlsx"
                                else:
                                    for nome_arquivo in os.listdir(self.path_gerado):
                                        if re.search(form_173_tudo[0][4], nome_arquivo):
                                            contador += 1
                                            new = self.path_gerado + "3- Form_Controle Aplicação Tinta "+ form_173_tudo[0]['cemb'] +" - "+ str(contador) + r".xlsx"
                                        else: new = self.path_gerado + "3- Form_Controle Aplicação Tinta "+ form_173_tudo[0]['cemb'] +" - "+ str(contador) + r".xlsx"
                            else:
                                print(form_173_tudo[0])
                                if os.listdir(self.path_gerado) == []:
                                    new = self.path_gerado + "3- Form_Controle Aplicação Tinta "+ form_173_tudo[0]['cemb'] +" - "+ str(contador) + r".xlsx"
                                else:
                                    for nome_arquivo in os.listdir(self.path_gerado):
                                        if re.search(form_173_tudo[0]["cemb"], nome_arquivo):
                                            contador += 1
                                            new = self.path_gerado + "3- Form_Controle Aplicação Tinta "+ form_173_tudo[0]['cemb'] +" - "+ str(contador) + r".xlsx"
                                        else: new = self.path_gerado + "3- Form_Controle Aplicação Tinta "+ form_173_tudo[0]['cemb'] +" - "+ str(contador) + r".xlsx"
                            if len(ocs) <= 15:
                                self.area = '$A$1:$K$56'
                                if os.path.exists(self.path_gerado):
                                    if os.path.isfile(str(new)):
                                        contador += 1
                                        shutil.copyfile(self.path, str(new))
                                    else: shutil.copyfile(self.path, str(new))
                                else: 
                                    if os.path.isfile(str(new)):
                                        contador += 1
                                        os.makedirs(self.path_gerado)
                                        shutil.copyfile(self.path, str(new))
                                    else: 
                                        os.makedirs(self.path_gerado)
                                        shutil.copyfile(self.path, str(new))
                            else:
                                self.area = '$A$1:$K$103'
                                if os.path.exists(self.path_gerado):
                                    if os.path.isfile(str(new)):
                                        contador += 1
                                        shutil.copyfile(self.path_maior, str(new))
                                    else: shutil.copyfile(self.path_maior, str(new))
                                else: 
                                    if os.path.isfile(str(new)):
                                        contador += 1
                                        os.makedirs(self.path_gerado)
                                        shutil.copyfile(self.path_maior, str(new))
                                    else:
                                        os.makedirs(self.path_gerado)
                                        shutil.copyfile(self.path_maior, str(new))
                        except:messagebox.showinfo(message='Provavelmente o código do operador está errado!')

                        excel_app = xw.App(visible=False)
                        wb = excel_app.books.open(new)  # connect to an existing file in the current working directory
                        wks = xw.sheets
                        ws = wks[0]
                        linha = 35
                        
                        for i in ocs:
                            padrao = i[1][:9]
                            oc = padrao + i[1].replace(padrao, '/')
                            print(i)
                            ws.range("F"+f"{linha}").value = oc
                            ws.range("I"+f"{linha}").value = i[2]
                            linha += 1
                            
                        ws.range("I4").value = DBForm_173.consultaEspecifica(idform173, 'Id_form_173')[0]['data_solicitacao'].format('%d.%m.%Y')
                        ws.range("C3").value = DBForm_161.ultimoId()
                        ws.range("C4").value = nome
                        ws.range("J3").value = form_173_tudo[0]['cemb']
                        ws.range("K4").value = form_173_tudo[0]['pintor']
                        
                        # # Definir a área de impressão
                        ws.api.PageSetup.PrintArea = self.area
                        
                        wb.save()
                        wb.close()
                        excel_app.quit()
                        # lista_impressoras = win32print.EnumPrinters(2) #printar isso pra descobrir a impressora!
                        # impressora = lista_impressoras[3]
                        
                        # win32print.SetDefaultPrinter(nomeImp) # Coloca em Default a impressora a ser utilizada
                        # win32api.ShellExecute(0, "print", "3- Form_Controle Aplicação Tinta "+form_173_tudo[0]['cemb'] +" - "+ str(contador) + r".xlsx", None, self.path_gerado, 0)
                        # self.finalizar(idform173)
                        # cursor.execute(f"UPDATE form_40 SET print={1} WHERE mescla='{mescla_n}'")
                        banco.commit()
                        cursor.close()
                        banco.close()
                        messagebox.showinfo(message="Impressão concluída!")
                        print("IMPRIMIU!!!")
                        self.destroy()
                    else: 
                        self.mainloop()
                        pass
                except Exception as ex: 
                    print("mescla3",ex)
                    messagebox.showerror(message=["mescla3",ex])

        self.mainloop()
    
    def atualizar(self):
        valor = len(pend_new.pend())
        self.ttk.Label_.config(text=f"{valor}  Solicitações Pendentes")

    def finalizar(self, id_form173):
        x = messagebox.askquestion(message="Deve finalizar?")
        if x =='yes':
            try:
                DBForm_173.update_form_173(id_form173, print=1)
            except Exception as ex: messagebox.showerror(message=ex)
        else: pass
