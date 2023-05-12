from DBfuncs import Operadores, DBForm_173, OCs

class DadosQuadros ():
    def __init__(self, status, data):
      self.status = status
      self.data = data
      self.listaQuadros = []
      
    def dados(self):
        dados = DBForm_173.conteudoTudoEspecifico(self.status, self.data)
        for i in dados:
            dictDados = i
            dictDados["ocs"] = OCs.consultaEspecifica(dictDados['id'], 'track_form173')
            self.listaQuadros.append(dictDados)
        return self.listaQuadros