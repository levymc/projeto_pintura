from flask import Blueprint, request, jsonify
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

@infosCEMB_bp.route("/infoViscosidade", methods=["GET", "POST"])
def infoViscosidade():
    dados = request.json
    visc_max_min = Relacao_Tintas.consultaViscosidade(dados['cemb'], dados['viscosimetro'])
    if int(dados['viscosidade']) >= visc_max_min[0] and int(dados['viscosidade']) <= visc_max_min[1]:
        return jsonify({"value": True})
    else:
        return jsonify({"error": "Valor de viscosidade inválido."}), 400

