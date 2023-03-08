import tkinter as tk
from tkinter import ttk

root = tk.Tk()

# Cria o widget Treeview
tree = ttk.Treeview(root, columns=('Nome', 'Idade'))

# Adiciona as colunas à tabela
tree.heading('#0', text='ID')
tree.heading('#1', text='Nome')
tree.heading('#2', text='Idade')

# Adiciona algumas linhas de exemplo
tree.insert('', 'end', text='1', values=('João', '30'))
tree.insert('', 'end', text='2', values=('Maria', '25'))
tree.insert('', 'end', text='3', values=('Pedro', '40'))

# Cria uma variável para armazenar as informações da linha selecionada
linha_selecionada = {}

# Define uma função para o botão que carrega as informações da linha selecionada
def carrega_linha_selecionada():
    # Obtém o ID da linha selecionada
    id_linha = tree.selection()[0]
    # Obtém as informações da linha selecionada
    info_linha = tree.item(id_linha)['values']
    # Armazena as informações na variável linha_selecionada
    linha_selecionada['nome'] = info_linha[0]
    linha_selecionada['idade'] = info_linha[1]
    # Exibe as informações na tela
    print(linha_selecionada)

# Cria o botão para carregar as informações da linha selecionada
btn_carregar = tk.Button(root, text='Carregar linha selecionada', command=carrega_linha_selecionada)
btn_carregar.pack()

# Exibe a tabela na tela
tree.pack()

root.mainloop()
