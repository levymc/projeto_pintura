from datetime import datetime
import xlwings as xw
import win32com.client as win32
import win32api
import sqlite3, shutil, win32print, re, os, local
from DBfuncs import DBForm_173, OCs, Operadores

form_173_tudo = DBForm_173.consultaEspecifica(89, 'id')
ocs = OCs.consultaEspecifica(89, 'track_form173')
nomePintor = Operadores.consultaEspecificaCodigo(form_173_tudo[0]['codPintor'])[0]['nome']
print(nomePintor)
