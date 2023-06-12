from flask import Blueprint, request, abort
from DBfuncs import Operadores, DBForm_173, OCs, DBForm_40, Relacao_Tintas
import hashlib, json


acesso_bp = Blueprint('acesso', __name__)


@acesso_bp.route("/acesso", methods=["POST", "GET"])
def acesso():
    userInput = request.json['usuario']
    passInput = request.json['senha']
    operador = Operadores.confereUsuario(userInput)
    if operador is None:
        print('Operador não encontrado.')
        return abort(404)
    elif operador.senha != hashlib.md5(passInput.encode()).hexdigest():
        print('Senha incorreta.')
        return abort(404)
    else:
        # renderiza a próxima tela
        print('Acesso concedido.')
        return "Ok"
    
@acesso_bp.route("/acessoProcesso", methods=["POST", "GET"])
def acessoProcesso():
    userInput = request.json['userInput']
    passInput = request.json['passInput']
    operador = Operadores.confereUsuario(userInput)
    if operador is None:
        print('Operador não encontrado.')
        return {"success": False}, abort(404)
    elif operador.senha != hashlib.md5(passInput.encode()).hexdigest():
        print('Senha incorreta.')
        return {"success": False}, abort(404)
    elif operador.priority != 'admin':
        print('Acesso negado. Somente usuários com prioridade "admin" podem acessar.')
        
        return {"success": False}, abort(403)
    else:
        # Renderiza a próxima tela
        print('Acesso concedido.')
        return {"success": True}