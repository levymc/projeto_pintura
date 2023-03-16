arg='prod'
computador = 2  # 1 é a Sala da Preparação, 2 Mascaramento e 3 meu computador

class Local():
    
    def local():
        return r'/pintura.db' if arg == "dev" else r'//NasTecplas/Pintura/DB/pintura.db' if "prod" else False
    
    def nomeImpressora():
        return 'RICOH MP C2504ex PCL 6' if computador == 3 else 'SP 3510DN PCL 6' if computador == 2 else 'RICOH Aficio SP 3510DN PCL' if computador == 1 else False
        
    
    
print(Local.nomeImpressora())
# print(Local.local('dev'))