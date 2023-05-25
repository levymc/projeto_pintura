from flask import Blueprint, request
from DBfuncs import Operadores, DBForm_173, OCs, DBForm_40, Relacao_Tintas
from interfaceDB import DadosQuadros

kaban = Blueprint('kaban', __name__)

@kaban.route("/dadosQuadrosHoje", methods=["POST", "GET"])
def dadosQuadrosHoje():
    status = request.args.get('status')
    data = request.args.get('data')
    return DadosQuadros(status, data).dados()

@kaban.route("/finalizarQuadro", methods=["POST"])
def finalizarQuadro():
    idForm173 = request.json["id"]
    return {"response": DBForm_173.update_form_173(idForm173, status=1)}

@kaban.route("/dadosQuadroId", methods=["GET", "POST"])
def dadosQuadroId():
    id = request.args.get("id")
    return DBForm_173.consultaEspecifica(id, "id")

@kaban.route("/dadosOcsId", methods=["GET", "POST"])
def dadosOcsId():
    id = request.args.get("track_form173")
    return OCs.consultaEspecifica(id, "track_form173")