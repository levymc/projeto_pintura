from datetime import datetime
import os

arg='dev'
computador = 3  # 1 é a Sala da Preparação, 2 Mascaramento e 3 meu computador

agora = datetime.today().strftime('%d.%m.%Y_%H.%M')
meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
anoAtual = agora[6:10]+"/"
mesAtual = meses[int(agora[3:5])-1]+"/"
dia_mesAtual = agora[:5]+"/"

class Local():
    
    def local():
        return r'pintura.db' if arg == "dev" else r'//NasTecplas/Pintura/DB/pintura.db' if "prod" else False
    
    def nomeImpressora():
        return 'RICOH MP C2504ex PCL 6' if computador == 3 else 'SP 3510DN PCL 6' if computador == 2 else 'RICOH Aficio SP 3510DN PCL 6' if computador == 1 else False
    
    def path():
        return r"./Forms/Form_161.xlsx" if arg == "dev" else r"//NasTecplas/Pintura/Forms/Form_161/Form_161.xlsx" if "prod" else False
    
    def path_maior():
        return r"./Forms/Form_161_maior.xlsx" if arg == "dev" else r"//NasTecplas/Pintura/Forms/Form_161/Form_161_maior.xlsx" if "prod" else False
    
    def path_gerado():
        return r"./Forms/Form_161_Gerado/"+anoAtual+mesAtual+dia_mesAtual if arg == "dev" else r"//NasTecplas/Pintura/Forms/Form_161/Form_161_Gerado/"+anoAtual+mesAtual+dia_mesAtual if "prod" else False

# print(os.path.exists(Local.path_gerado()))   
    
    
# print(Local.nomeImpressora())
# print(Local.local('dev'))
