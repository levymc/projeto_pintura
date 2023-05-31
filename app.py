from flask import Flask, render_template, request, flash, abort
from waitress import serve
from DBfuncs import Operadores, DBForm_173, OCs, DBForm_40, Relacao_Tintas
import hashlib
import json
from interfaceDB import DadosQuadros
from print161 import Print161
from routes.infosCEMB import *
from routes.kaban import *
from routes.ultimaMescla import *
from routes.newMEP import *

mode = "dev" #prod ou dev

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


app.register_blueprint(infosCEMB_bp)
app.register_blueprint(kaban)
app.register_blueprint(insertDB_newMEP)
app.register_blueprint(ultimaMescla_bp)


@app.route("/", methods=["POST", "GET"])
def index():
    return render_template('index.html')

@app.route("/acesso", methods=["POST", "GET"])
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
    
@app.route("/acessoProcesso", methods=["POST", "GET"])
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


@app.route("/form173_inserir", methods=["POST", "GET"])
def form173_inserir():
    dados = request.json
    dadosInserir = {
        'numeroForm': dados['numeroForm'],
        'solicitante': dados['solicitante'],
        'codPintor': dados['codPintor'],
        'cemb': dados['cemb'],
        'quantidade': dados['quantidade'],
        'unidade': dados['unidade'],
        'data': dados['data'],
        'status': dados['status'],
        'mescla': dados['mescla']
    }
    objetoInserido = DBForm_173.insert(dadosInserir)
    return {
        "success": True,
        "obj": objetoInserido
    }
    
@app.route("/ocs_inserir", methods=["POST", "GET"])
def ocs_inserir():
    dados = request.json
    print(dados)
    ocsInseridas = OCs.insertOC(dados['id_form173'], dados['ocs'])
    return {"success": True}

@app.route("/ocs_remove", methods=["POST", "GET"])
def ocs_remove():
    dados = request.json
    print(dados)
    OCs.removeOC(dados['idOC'])
    return {"success": True}

@app.route("/form40_inserir", methods=["POST", "GET"])
def form40_inserir():
    dados = request.json
    print(dados)
    DBForm_40.insert(**dados)
    return {"success": True}

@app.route("/viscosimetro", methods=("POST", "GET"))
def viscosimetro():
    cemb = request.args.get("cemb")
    return Relacao_Tintas.consultaViscosimetro(cemb)

@app.route("/print161", methods=["POST", "GET"])
def print161():
    idForm73 = request.json['id']
    user = request.json['user']
    impressora = request.json['impressora']
    Print161(idForm73, user, impressora)
    return {"success": True}




if __name__ == '__main__':
    if mode == 'dev':
        app.run(debug=True, host='0.0.0.0', port=5005)
    else:
        serve(app, host='0.0.0.0', port=5005, threads=1, url_scheme='https')