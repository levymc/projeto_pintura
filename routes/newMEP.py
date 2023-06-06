from flask import Blueprint, request
from DBfuncs import Relacao_Tintas


insertDB_newMEP = Blueprint('newMEP', __name__)

@insertDB_newMEP.route("/newMEP", methods=["POST", "GET"])
def newMEP():
    dados = request.json
    if 'newMEP_adicionar' in dados and 'imageProp' in dados:
        return Relacao_Tintas.insert({
            'cemb': dados['newCEMB'],
            'descricao': dados['newDescription'],
            'norma': 'MEP'+dados['newMEP_adicionar'].replace("MEP", ''),
            'graph': dados['imageProp'],
            })
    else:
        return Relacao_Tintas.insert({
            'cemb': dados['newCEMB'],
            'descricao': dados['newDescription'],
            'norma': 'MEP'+dados['newMEP'].replace("MEP", ''),
            })