from flask import Blueprint, request
from DBfuncs import Operadores, DBForm_173, OCs, DBForm_40, Relacao_Tintas


insertDB_newMEP = Blueprint('newMEP', __name__)

@insertDB_newMEP.route("/newMEP", methods=["POST", "GET"])
def newMEP():
    dados = request.json
    print("EU",dados)
    if 'newMEP_adicionar' in dados and 'imageProp' in dados:
        return Relacao_Tintas.insert({
            'cemb': dados['newCEMB'],
            'norma': dados['newMEP_adicionar'],
            'graph': dados['imageProp'],
            })
    else:
        return Relacao_Tintas.insert({
            'cemb': dados['newCEMB'],
            'norma': dados['newMEP'],
            })