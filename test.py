import os

pasta_raiz = r'\\NasTecplas\Pintura\Forms\Form_161\Form_161_Gerado'
lista_arquivos_xlsx = []

for pasta_atual, sub_pastas, arquivos in os.walk(pasta_raiz):
    for arquivo in arquivos:
        if arquivo.endswith('.xlsx'):
            lista_arquivos_xlsx.append([arquivo,pasta_atual])

for i in lista_arquivos_xlsx:
    print(i)