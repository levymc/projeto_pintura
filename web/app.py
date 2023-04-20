from flask import Flask, render_template, request, flash
from waitress import serve
from DBfuncs import Operadores

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
    print(userInput, passInput)
    return {"usuario": userInput,
            "senha": passInput}

if __name__ == '__main__':
    if mode == 'dev':
        app.run(debug=True, host='0.0.0.0', port=5005)
    else:
        serve(app, host='0.0.0.0', port=5005, threads=5, url_scheme='https')