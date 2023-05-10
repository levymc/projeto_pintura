from flask import Flask, render_template, request, flash, abort
from waitress import serve
from DBfuncs import Operadores, DBForm_173, OCs
import hashlib
import json

mode = "dev" #prod ou dev

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

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
        #renderiza a próxima tela
        print('Acesso concedido.')
        return "Ok"

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
        'status': dados['status']
    }
    objetoInserido = DBForm_173.insert(dadosInserir)
    # print(json.dumps(objetoInserido.to_dict()))
    return {
        "success": True,
        "obj": objetoInserido.to_dict()
    }
    
@app.route("/ocs_inserir", methods=["POST", "GET"])
def ocs_inserir():
    dados = request.json
    print(dados)    
    ocsInseridas = OCs.insertOC(dados['id_form173'], dados['ocs'])
    return {"success": True}

@app.route("/dadosQuadrosHoje", methods=["POST", "GET"])
def dadosQuadrosHoje():
    listaQuadros = []
    status = request.args.get('status')
    data = request.args.get('data')
    dados = DBForm_173.conteudoTudoEspecifico(status, data)
    for i in dados:
        dictDados = i()
        dictDados["ocs"] = OCs.consultaEspecifica(dictDados['id'], 'track_form173')
        listaQuadros.append(dictDados)
    return listaQuadros



if __name__ == '__main__':
    if mode == 'dev':
        app.run(debug=True, host='0.0.0.0', port=5005)
    else:
        serve(app, host='0.0.0.0', port=5005, threads=5, url_scheme='https')