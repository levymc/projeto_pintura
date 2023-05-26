from flask import Blueprint, request
from DBfuncs import Operadores, DBForm_173, OCs, DBForm_40, Relacao_Tintas


insertDB_newMEP = Blueprint('newMEP', __name__)

@insertDB_newMEP.route("/newMEP", methods=["POST", "GET"])
def newMEP():
    dados = request.json
    print(dados)
    return {'value': True}