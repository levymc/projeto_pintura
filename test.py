from DBfuncs import DBForm_40

mescla = DBForm_40.consultaEspecifica('Id_form_40', DBForm_40.obter_ultima_linha()['Id_form_40'])
print(mescla)