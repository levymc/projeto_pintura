from flask import Blueprint, request
from DBfuncs import Operadores, DBForm_173, OCs, DBForm_40, Relacao_Tintas


infosCEMB_bp = Blueprint('infosCEMB', __name__)

@infosCEMB_bp.route("/infosCEMB", methods=["POST", "GET"])
def infosCEMB():
    cemb = request.json.get('cemb', '')
    if Relacao_Tintas.consultaEspecifica(cemb, 'cemb') == []:
        return False
    else:
        return Relacao_Tintas.consultaEspecifica(cemb, 'cemb')


@infosCEMB_bp.route("/allInfoCEMB", methods=["GET"])
def allInfoCEMB():
    return Relacao_Tintas.consulta()

