from flask import Flask, render_template, request, flash, abort
from waitress import serve
from DBfuncs import Operadores, DBForm_173, OCs, DBForm_40, Relacao_Tintas
import hashlib
import json
from interfaceDB import DadosQuadros

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
    return {
        "success": True,
        "obj": objetoInserido
    }
    
@app.route("/ocs_inserir", methods=["POST", "GET"])
def ocs_inserir():
    dados = request.json
    ocsInseridas = OCs.insertOC(dados['id_form173'], dados['ocs'])
    return {"success": True}

@app.route("/dadosQuadrosHoje", methods=["POST", "GET"])
def dadosQuadrosHoje():
    status = request.args.get('status')
    data = request.args.get('data')
    return DadosQuadros(status, data).dados()

@app.route("/finalizarQuadro", methods=["POST"])
def finalizarQuadro():
    idForm173 = request.json["id"]
    return {"response": DBForm_173.update_form_173(idForm173, status=1)}

@app.route("/dadosQuadroId", methods=["GET", "POST"])
def dadosQuadroId():
    id = request.args.get("id")
    return DBForm_173.consultaEspecifica(id, "id")

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



if __name__ == '__main__':
    if mode == 'dev':
        app.run(debug=True, host='0.0.0.0', port=5005)
    else:
        serve(app, host='0.0.0.0', port=5005, threads=1, url_scheme='https')