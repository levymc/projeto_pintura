import os
from datetime import datetime

agora = datetime.today().strftime('%d.%m.%Y_%H.%M')
meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
anoAtual = agora[6:10]+"/"
mesAtual = meses[int(agora[3:5])-1]+"/"
dia_mesAtual = agora[:5]+"/"


path_gerado = r"C:/Users/levym/OneDrive/Documentos/Projects/Tecplas/Sis-Pint/projeto_pintura/Forms/Form_161_Gerado/" + anoAtual + mesAtual + dia_mesAtual

if os.path.exists(path_gerado):
     print('a')
else: 
    print(1)
    os.makedirs(path_gerado)
    print('b')