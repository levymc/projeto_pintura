import hashlib, json, sqlite3

def opcoesViscosimetros():
        opcoesViscosimetros = []
        try:
            banco = sqlite3.connect("pintura.db")
            cursor = banco.cursor()
            cemb_tinta = cursor.execute(f"SELECT cemb FROM form_173 WHERE Id_form_173 = 1").fetchall()[0][0]
            new_cemb = ''
            for i in cemb_tinta:
                if not i=="E":
                    new_cemb += i
            opcoes = cursor.execute(f"SELECT viscosimetro FROM relacao_tintas WHERE cemb = 1453042").fetchall() #{int(new_cemb)}
            cursor.close()
            banco.close()
            
            for copo in opcoes:
                opcoesViscosimetros.append(copo[0])
            
            return opcoesViscosimetros
        except Exception as ex:
            print("Error: ", ex, type(ex))
                
print(opcoesViscosimetros())