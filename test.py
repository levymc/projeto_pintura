import os, re
from datetime import datetime

# Define a pasta raiz
root_folder = r'\\NasTecplas\Pintura\Forms\Form_161\Form_161_Gerado'

# Define a lista para salvar os nomes dos arquivos e seus caminhos
arquivos_excel = []
padrao = re.compile(r"3- Form_Controle Aplicação Tinta (\d+ - \d+)\.xlsx")
# Percorre todas as pastas e arquivos dentro da pasta raiz
for pasta_atual, sub_pastas, arquivos in os.walk(root_folder):
    # Percorre todos os arquivos na pasta atual
    for arquivo in arquivos:
        # Verifica se o arquivo é um arquivo Excel (.xlsx)
        if arquivo.endswith('.xlsx'):
            # Obtém o caminho completo do arquivo
            caminho_arquivo = os.path.join(pasta_atual, arquivo)
            # Obtém a data atual
            data_atual = datetime.now()
            # Obtém o ano, mês e dia atual em diferentes formatos
            ano_atual = data_atual.strftime('%Y')
            mes_atual = data_atual.strftime('%m')
            dia_atual = data_atual.strftime('%d.%m')
            mes_atual_escrito = data_atual.strftime('%B')
            # Cria o caminho da pasta para este arquivo
            caminho_pasta = os.path.join(root_folder, ano_atual, mes_atual_escrito, dia_atual)
            # Adiciona o nome do arquivo e o caminho da pasta à lista
            match = padrao.search(arquivo)
            if match:
                codigo = match.group(1)
                # codigos.append(codigo)
                form161.tree.insert('', 'end', text='1', values=(arquivo, caminho_pasta))
                arquivos_excel.append([codigo, caminho_pasta])


# codigos = []
# padrao = re.compile(r"3- Form_Controle Aplicação Tinta (\d+ - \d+)\.xlsx")

# for nome_arquivo in arquivos_excel:
#     print(nome_arquivo)
#     match = padrao.search(nome_arquivo[0])
#     if match:
#         codigo = match.group(1)
#         codigos.append(codigo)

for i in arquivos_excel:
    print(i)
