from tkinter import *
from tkinter import messagebox, ttk
import tkinter as tk
from DBfuncs import DBForm_173,DBForm_40
from ttkbootstrap import Style as BsStyle
import tkinter.font as font
import os, re, subprocess
from OC_ex import OC_ex
from datetime import datetime


class MaisInfo(Toplevel):
    janela_aberta = False
    def __init__(info):
        if not MaisInfo.janela_aberta:
            MaisInfo.janela_aberta = True
            super().__init__()
            info.protocol("WM_DELETE_WINDOW", lambda: info.on_closing())
            info.geometry("400x400")
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
                           wraplength=300, background='#f0f5ff', justify=['center'])
        titulo.pack(pady=20)
        
        # Botão de vizualização dos Form173 finalizados
        btn_infoForm173 = ttk.Button(info, text='Form173', style='Custom.TButton', command=lambda:VisuForm173())
        btn_infoForm173.pack(pady=20, padx=(0,0))
        
        # Botão de vizualização dos Form40 finalizados
        btn_infoForm40 = ttk.Button(info, text='Form40', style='Custom.TButton', command=lambda:VisuForm40())
        btn_infoForm40.pack(pady=20, padx=(0,0))
        
        # Botão de vizualização dos Form40 finalizados
        btn_infoForm161 = ttk.Button(info, text='Form161', style='Custom.TButton', command=lambda:VisuForm163())
        btn_infoForm161.pack(pady=20, padx=(0,0))
        

class VisuForm173(Toplevel): 
    def __init__(form173):
        super().__init__()
        form173.geometry("450x350")
        form173.configure(background='#c5d3f0')
        form173.iconbitmap(r'logo.ico')
        form173.resizable(0,0)
        form173.title('Solicitações Pendentes')
        form173.create_wigets()
        
    def create_wigets(form173):
        titulo = ttk.Label(form173, text="Solicitações de Tinta ainda Pendentes", style='TituloMenor.TLabel',
                           wraplength=300, background='#c5d3f0', justify=['center'])
        titulo.pack(pady=20)
        
        form173.tree = ttk.Treeview(form173, columns=('id', 'Formulário', 'Solicitante', 'Data', 'CEMB', 'Quantidade'))
        form173.tree.column('#0',width=0, minwidth=0)
        form173.tree.column('#1',width=20, minwidth=30, anchor=CENTER)
        form173.tree.column('#2',width=80, anchor=tk.CENTER)
        form173.tree.column('#3',width=80, anchor=tk.CENTER)
        form173.tree.column('#4',width=80, anchor=tk.CENTER)
        form173.tree.column('#5',width=80, anchor=tk.CENTER)
        form173.tree.column('#6',width=80, anchor=tk.CENTER)
        
        # Adiciona as colunas à tabela
        form173.tree.heading('#0', text='ID')
        form173.tree.heading('#1', text='id')
        form173.tree.heading('#2', text='Formulário')
        form173.tree.heading('#3', text='Solicitante')
        form173.tree.heading('#4', text='Data')
        form173.tree.heading('#5', text='CEMB')
        form173.tree.heading('#6', text='Quantidade')
        
        for i in DBForm_173.conteudoTudo(1): #Adicionando linhas na tabela
            form173.tree.insert('', 'end', text='1', values=(i['Id_form_173'], i['formulario'], i['solicitante'],
                                                          i['data_solicitacao'], i['cemb'], str(i['quantidade'])+i['unidade']))
        form173.tree.pack()


class VisuForm40(Toplevel): 
    def __init__(form40):
        super().__init__()
        form40.screen_width = form40.winfo_screenheight()
        form40.geometry(f"{form40.screen_width}x400")
        form40.configure(background='#b4bbcc')
        form40.iconbitmap(r'logo.ico')
        form40.resizable(0,0)
        form40.title('Solicitações Pendentes')
        form40.create_wigets()
        
    def create_wigets(form40):
        titulo = ttk.Label(form40, text="Solicitações de Tinta ainda Pendentes", style='TituloMenor.TLabel',
                           wraplength=300, background='#b4bbcc', justify=['center'])
        titulo.pack(pady=20)
        
        # tableFrame = ttk.Frame(form40, )
        
        form40.tree = ttk.Treeview(form40, columns=('id', 'Mescla', 'Data', 'Temperatura', 'Umidade', 'CEMB',
                                                    'Lote', 'Validade', 'Viscosímetro', 'Viscosidade', 'Proporção',
                                                    'Pot Life', 'Responsável', 'Id_Form173', 'Imprimiu?', 'Exceção?'
                                                    ))
        form40.tree.column('#0',width=0, minwidth=0)
        form40.tree.column('#1',width=20, minwidth=30, anchor=CENTER)
        form40.tree.column('#2',width=80, anchor=tk.CENTER)
        form40.tree.column('#3',width=80, anchor=tk.CENTER)
        form40.tree.column('#4',width=80, anchor=tk.CENTER)
        form40.tree.column('#5',width=80, anchor=tk.CENTER)
        form40.tree.column('#6',width=80, anchor=tk.CENTER)
        form40.tree.column('#7',width=80, anchor=tk.CENTER)
        form40.tree.column('#8',width=80, anchor=tk.CENTER)
        form40.tree.column('#9',width=80, anchor=tk.CENTER)
        form40.tree.column('#10',width=80, anchor=tk.CENTER)
        form40.tree.column('#11',width=80, anchor=tk.CENTER)
        form40.tree.column('#12',width=80, anchor=tk.CENTER)
        form40.tree.column('#13',width=80, anchor=tk.CENTER)
        form40.tree.column('#14',width=80, anchor=tk.CENTER)
        form40.tree.column('#15',width=80, anchor=tk.CENTER)
        form40.tree.column('#16',width=80, anchor=tk.CENTER)
        
        # Adiciona as colunas à tabela
        form40.tree.heading('#0', text='ID')
        form40.tree.heading('#1', text='id')
        form40.tree.heading('#2', text='Mescla')
        form40.tree.heading('#3', text='Data')
        form40.tree.heading('#4', text='Temperatura')
        form40.tree.heading('#5', text='Umidade')
        form40.tree.heading('#6', text='CEMB')
        form40.tree.heading('#7', text='Lote')
        form40.tree.heading('#8', text='Validade')
        form40.tree.heading('#9', text='Viscosímetro')
        form40.tree.heading('#10', text='Viscosidade')
        form40.tree.heading('#11', text='Proporção')
        form40.tree.heading('#12', text='Pot Life')
        form40.tree.heading('#13', text='Responsável')
        form40.tree.heading('#14', text='Id_Form173')
        form40.tree.heading('#15', text='Imprimiu?')
        form40.tree.heading('#16', text='Exceção?')
        
        # Adicionando as linhas da tabela, puxando do banco
        for i in DBForm_40.consulta(): #Adicionando linhas na tabela
            form40.tree.insert('', 'end', text='1', values=(i['Id_form_40'], i['mescla'], i['data_prep'], i['temperatura'], i['umidade'],
                                                          i['cod_mp'], i['lotemp'], i['shelf_life'], i['viscosimetro'], i['viscosidade'],
                                                          ['proporcao'], i['pot_life'], i['responsavel'], i['Id_form173'], i['print'],i['excessao']))
        form40.tree.pack(padx=10)
        
        # Cria a barra de rolagem horizontal
        xscrollbar = ttk.Scrollbar(form40, orient='horizontal', command=form40.tree.xview)
        form40.tree.configure(xscrollcommand=xscrollbar.set)
        xscrollbar.pack(fill=X, padx=10,pady=5)

        # Cria o botão para carregar as informações da linha selecionada
        btn_carregar = ttk.Button(form40, text='...', style='Att.TButton') #, command=lambda:form40.carrega_linha_selecionada()
        btn_carregar.pack(pady=25, padx=(0,0))
        
        

class VisuForm163(Toplevel):
    def __init__(form161):
        super().__init__()
        form161.geometry("800x370")
        form161.configure(background='#b1b2b5')
        form161.iconbitmap(r'logo.ico')
        form161.resizable(0,0)
        form161.title('Solicitações Pendentes')
        form161.create_wigets()
    
    def create_wigets(form161):
        titulo = ttk.Label(form161, text="Solicitações de Tinta ainda Pendentes", style='TituloMenor.TLabel',
                           wraplength=300, background='#b1b2b5', justify=['center'])
        titulo.pack(pady=20)
        
        form161.tree = ttk.Treeview(form161, columns=('id', 'Arquivo', 'Caminho'))
        form161.tree.column('#0',width=0, minwidth=0)
        form161.tree.column('#1',width=0, minwidth=0, anchor=CENTER)
        form161.tree.column('#2',width=100, minwidth=30, anchor=CENTER)
        form161.tree.column('#3',width=420, anchor=tk.CENTER)
        
        # Adiciona as colunas à tabela
        form161.tree.heading('#0', text='ID')
        form161.tree.heading('#1', text='Original')
        form161.tree.heading('#2', text='Arquivo')
        form161.tree.heading('#3', text='Caminho')
        
        padrao = re.compile(r"3- Form_Controle Aplicação Tinta (\d+ - \d+)\.xlsx")
        pasta_raiz = r'\\NasTecplas\Pintura\Forms\Form_161\Form_161_Gerado'
        lista_arquivos_xlsx = []
        for pasta_atual, sub_pastas, arquivos in os.walk(pasta_raiz):
            for arquivo in arquivos:
                if arquivo.endswith('.xlsx'):
                    lista_arquivos_xlsx.append([arquivo,pasta_atual])
                    match = padrao.search(arquivo)
                    if match:
                        codigo = match.group(1)
                        form161.tree.insert('', 'end', text='1', values=(arquivo, codigo, pasta_atual))
        # Cria a scrollbar e a vincula à Treeview
        scrollbar = ttk.Scrollbar(form161, orient="vertical", command=form161.tree.yview)
        form161.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", ipady=100, pady=(0, 105),padx=(0,105))
        form161.tree.pack(padx=(100, 0))
        

        # Cria os botões para carregar as informações da linha selecionada
        btn_abrirPasta = ttk.Button(form161, text='Abrir Pasta', command=lambda:form161.abrir_pasta_selecionada(), style='Att.TButton') #, command=lambda:form40.carrega_linha_selecionada()
        btn_abrirPasta.pack(side='left', pady=25, padx=(300,5))
        btn_abrirArquivo = ttk.Button(form161, text='Abrir Arquivo', command=lambda:form161.abrir_arquivo_selecionado(), style='Att.TButton')
        btn_abrirArquivo.pack(side='right', pady=25, padx=(0,200))

                
    def abrir_pasta_selecionada(form161):
        # Obtém a linha selecionada na tabela
        item_id = form161.tree.focus()
        # Obtém o valor da segunda coluna da linha selecionada
        caminho_pasta = form161.tree.item(item_id)['values'][1]
        # Abre o explorador de arquivos na pasta desejada
        subprocess.Popen(f'explorer "{caminho_pasta}"')

    def abrir_arquivo_selecionado(form161):
        # Obtém a linha selecionada na tabela
        item_id = form161.tree.focus()
        # Obtém o valor da segunda coluna da linha selecionada
        caminho_arquivo = os.path.join(form161.tree.item(item_id)['values'][2], form161.tree.item(item_id)['values'][0])
        # Abre o arquivo desejado
        os.startfile(caminho_arquivo)
