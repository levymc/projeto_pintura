from flask import Blueprint, request, abort
from DBfuncs import Operadores, DBForm_173, OCs, DBForm_40, Relacao_Tintas
import hashlib, json


operadores_bp = Blueprint('operadores', __name__)

@operadores_bp.route("/confereCOD", methods=["POST", "GET"])
def confereCOD():
    codPintor = request.json.get('codPintor', '')
    if Operadores.consultaEspecificaCodigo(codPintor) == []:
        return False
    else:
        return Operadores.consultaEspecificaCodigo(codPintor)