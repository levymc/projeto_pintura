from flask import Blueprint, request
from DBfuncs import Operadores, DBForm_173, OCs, DBForm_40, Relacao_Tintas


ultimaMescla_bp = Blueprint('ultimaMescla', __name__)

@ultimaMescla_bp.route("/obterUltimaMescla", methods=["POST", "GET"])
def ultimaMescla():
    return DBForm_173.get_ultima_linha_form173()
