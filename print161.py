from datetime import datetime
import xlwings as xw
import win32com.client as win32
import win32api
import sqlite3, shutil, win32print, re, os, local
from DBfuncs import DBForm_173, OCs, Operadores



class Mesclas():
    def __init__(self):
        super().__init__()
        self.path = local.Local.path()
        self.path_maior = local.Local.path_maior()
        self.path_gerado = local.Local.path_gerado()
        self.form_173_tudo = DBForm_173.consultaEspecifica(89, 'id')
        self.ocs = OCs.consultaEspecifica(89, 'track_form173')
        self.nomePintor = Operadores.consultaEspecificaCodigo(self.form_173_tudo[0]['codPintor'])[0]['nome']
        self.contador = 1

    def directory(self):
        if not os.path.exists(self.path_gerado):
            os.makedirs(self.path_gerado)
            print("CRIANDO O DIR: ",self.path_gerado)
            if os.listdir(self.path_gerado) == []:
                self.new = self.path_gerado + "3- Form_Controle Aplicação Tinta "+ self.form_173_tudo[0]['cemb'] +" - "+ str(self.contador) + r".xlsx"
            else:
                for nome_arquivo in os.listdir(self.path_gerado):
                    if re.search(self.form_173_tudo[0][4], nome_arquivo):
                        self.contador += 1
                        self.new = self.path_gerado + "3- Form_Controle Aplicação Tinta "+ self.form_173_tudo[0]['cemb'] +" - "+ str(self.contador) + r".xlsx"
                    else: self.new = self.path_gerado + "3- Form_Controle Aplicação Tinta "+ self.form_173_tudo[0]['cemb'] +" - "+ str(self.contador) + r".xlsx"
        else:
            if os.listdir(self.path_gerado) == []:
                self.new = self.path_gerado + "3- Form_Controle Aplicação Tinta "+ self.form_173_tudo[0]['cemb'] +" - "+ str(self.contador) + r".xlsx"
            else:
                for nome_arquivo in os.listdir(self.path_gerado):
                    if re.search(self.form_173_tudo[0]["cemb"], nome_arquivo):
                        self.contador += 1
                        self.new = self.path_gerado + "3- Form_Controle Aplicação Tinta "+ self.form_173_tudo[0]['cemb'] +" - "+ str(self.contador) + r".xlsx"
                    else: self.new = self.path_gerado + "3- Form_Controle Aplicação Tinta "+ self.form_173_tudo[0]['cemb'] +" - "+ str(self.contador) + r".xlsx"
        self.copyFiles()
    
    def copyFiles(self):
        pass
                                        
# Mesclas().directory()
print(len(OCs.consultaEspecifica(89, 'track_form173')))
  