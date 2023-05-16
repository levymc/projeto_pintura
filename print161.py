from datetime import datetime
import xlwings as xw
import win32com.client as win32
import win32api
import sqlite3, shutil, win32print, re, os, local
from DBfuncs import DBForm_173, OCs, Operadores

nomeImp = local.Local.nomeImpressora()

class Print161():
    def __init__(self, idPassado):
        super().__init__()
        self.path = local.Local.path()
        self.id = idPassado
        self.path_maior = local.Local.path_maior()
        self.path_gerado = local.Local.path_gerado()
        self.form_173_tudo = DBForm_173.consultaEspecifica(self.id, 'id') 
        self.ocs = OCs.consultaEspecifica(self.id, 'track_form173')
        self.nomePintor = Operadores.consultaEspecificaCodigo(self.form_173_tudo[0]['codPintor'])[0]['nome']
        self.codPintor = self.form_173_tudo[0]['codPintor']
        self.contador = 1
        self.new = ''
        self.directory()

    def directory(self):
        if not os.path.exists(self.path_gerado):
            os.makedirs(self.path_gerado)
            print("CRIANDO O DIR: ",self.path_gerado)
            if os.listdir(self.path_gerado) == []:
                self.new = self.path_gerado + "3- Form_Controle Aplicação Tinta "+ str(self.form_173_tudo[0]['cemb']) +" - "+ str(self.contador) + r".xlsx"
            else:
                for nome_arquivo in os.listdir(self.path_gerado):
                    if re.search(self.form_173_tudo[0][4], nome_arquivo):
                        self.contador += 1
                        self.new = self.path_gerado + "3- Form_Controle Aplicação Tinta "+ str(self.form_173_tudo[0]['cemb']) +" - "+ str(self.contador) + r".xlsx"
                    else: self.new = self.path_gerado + "3- Form_Controle Aplicação Tinta "+ str(self.form_173_tudo[0]['cemb']) +" - "+ str(self.contador) + r".xlsx"
        else:
            if os.listdir(self.path_gerado) == []:
                self.new = self.path_gerado + "3- Form_Controle Aplicação Tinta "+ str(self.form_173_tudo[0]['cemb']) +" - "+ str(self.contador) + r".xlsx"
            else:
                for nome_arquivo in os.listdir(self.path_gerado):
                    if re.search(str(self.form_173_tudo[0]["cemb"]), nome_arquivo):
                        self.contador += 1
                        self.new = self.path_gerado + "3- Form_Controle Aplicação Tinta "+ str(self.form_173_tudo[0]['cemb']) +" - "+ str(self.contador) + r".xlsx"
                    else: self.new = self.path_gerado + "3- Form_Controle Aplicação Tinta "+ str(self.form_173_tudo[0]['cemb']) +" - "+ str(self.contador) + r".xlsx"
        self.copyFiles()
    
    def copyFiles(self):
        if len(self.ocs) <= 15:
            self.area = '$A$1:$K$56'
            if os.path.exists(self.path_gerado):
                if os.path.isfile(str(self.new)):
                    self.contador += 1
                    shutil.copyfile(self.path, str(self.new))
                else: shutil.copyfile(self.path, str(self.new))
            else: 
                if os.path.isfile(str(self.new)):
                    self.contador += 1
                    os.makedirs(self.path_gerado)
                    shutil.copyfile(self.path, str(self.new))
                else: 
                    os.makedirs(self.path_gerado)
                    shutil.copyfile(self.path, str(self.new))
        else:
            self.area = '$A$1:$K$103'
            if os.path.exists(self.path_gerado):
                if os.path.isfile(str(self.new)):
                    self.contador += 1
                    shutil.copyfile(self.path_maior, str(self.new))
                else: shutil.copyfile(self.path_maior, str(self.new))
            else: 
                if os.path.isfile(str(self.new)):
                    self.contador += 1
                    os.makedirs(self.path_gerado)
                    shutil.copyfile(self.path_maior, str(self.new))
                else:
                    os.makedirs(self.path_gerado)
                    shutil.copyfile(self.path_maior, str(self.new))
        self.insertInfos()
                                      
    def insertInfos(self):
        excel_app = xw.App(visible=False)
        wb = excel_app.books.open(self.new)  # connect to an existing file in the current working directory
        wks = xw.sheets
        ws = wks[0]
        linha = 35
        
        for i in self.ocs:
            padrao = str(i['oc'])[:9]
            oc = padrao + str(i['oc']).replace(padrao, '/')
            print(i)
            ws.range("F"+f"{linha}").value = oc
            ws.range("I"+f"{linha}").value = i['quantidade']
            linha += 1
        # print(idAgora)
        # print(DBForm_173.consultaEspecifica(idAgora, 'Id_form_173'))
        # DBForm_161.insert(idAgora, 1)
        ws.range("I4").value = DBForm_173.consultaEspecifica(self.id, 'id')[0]['data'].format('%d.%m.%Y')
        ws.range("C3").value = "Mescla"
        ws.range("C4").value = self.nomePintor
        ws.range("J3").value = self.form_173_tudo[0]['cemb']
        ws.range("K4").value = self.codPintor
        
        # # Definir a área de impressão
        ws.api.PageSetup.PrintArea = self.area
        
        wb.save()
        wb.close()
        excel_app.quit()  
        
        win32print.SetDefaultPrinter(nomeImp) # Coloca em Default a impressora a ser utilizada
        win32api.ShellExecute(0, "print", "3- Form_Controle Aplicação Tinta "+ str(self.form_173_tudo[0]['cemb']) +" - "+ str(self.contador) + r".xlsx", None, self.path_gerado, 0)
        
# Print161(89)
print(OCs.consultaEspecifica(161, 'track_form173'))
ocs = OCs.consultaEspecifica(161, 'track_form173')[1]['oc']
padrao = str(ocs)[:9]
oc = padrao + str(ocs).replace(padrao, '/')
# print(oc)
