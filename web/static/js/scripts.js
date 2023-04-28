// Variáveis Globais
let container = document.querySelector(".container");
let user ;
let ocsAdded = [];

let enterKeyHandler = function(event) {
    if (event.key === "Enter") {
        acessoUserForm();
    }
};


let renderizarLogin = () => {
    container.innerHTML = '';
    container.innerHTML = `
    <div class="userForm flex">
        <input class="userInput" name="userInput" type="text" placeholder="Usuário">
        <input class="passInput" name="passInput" type="password" placeholder="Senha">
        <button onclick="acessoUserForm()" id="btn-userForm">Entrar</button>
    </div>`
    document.addEventListener("keydown", enterKeyHandler);
};

let acessoUserForm = () => {    
    let userInput = document.querySelector(".userInput").value;
    let passInput = document.querySelector(".passInput").value;
    user = userInput;
    axios.post("/acesso", {
        usuario: userInput,
        senha: passInput,
    }).then(response => {
        console.log(response);
        document.removeEventListener("keydown", enterKeyHandler);
        renderizarMain();
    }).catch(error => {
        console.log(error);
        alert("Ocorreu algum erro, tente novamente ou acione o Processo.")
    })
}

let renderizarMain = () => {
    container.innerHTML = '';
    container.innerHTML += `
            <div class="menu-superior">
                <button onclick="renderizarForm173()">Solicitação de Tinta</button>
                <button onclick="renderizarForm40()">Preparação da Tinta</button>
                <button onclick="renderizarForm161()">Aplicação da Tinta</button>
            </div>
            <div class="conteudo"></div>
    `
}

let renderizarForm173 = () => {
    let conteudo = document.querySelector(".conteudo");
    conteudo.innerHTML = '';
    conteudo.innerHTML += `
    <div class="conteudo-form173">
        <div class="form173">
            <div class="solicitante">
                <h3>Solicitante: ${user}</h3>
            </div>
            <div class="numeroForm">
                <input type="text" placeholder="Formulário Nº">
            </div>
            <div class="codPintor">
                <input type="number" placeholder="Código do Pintor">
            </div>
            <div class="cemb">
                <input type="number" placeholder="CEMB">
            </div>
            <div class="quantidade">
                <input type="number" placeholder="Quantidade Solicitada">
                <div class="checkboxes">
                    <label for="ml">ml</label>
                    <input type="checkbox" name='ml' value="ml" class="ml-checkbox">
                    <label for="g">g</label>
                    <input type="checkbox" name='g' value="g" class="g-checkbox">
                </div>
            </div>
        </div>
        <div class="ocsForm173">
            <div class="campoOC">
                <input type="number" placeholder="OC" class="oc_solicitada">
                <input type="number" placeholder="Quantidade" class="qnt_solicitada">
            </div>
            <div class="btnAddOC"><button onclick="btnAddOC()">Adicionar OC</button></div>
            <table class="listaOCs">
                <tr>
                    <th>OC</th>
                    <th>Quantidade</th>
                </tr>
            </table>
            <div class="contadorOCs"></div>
        </div>
    </div>
    `;
    let mlCheckBox = document.querySelector(".ml-checkbox");
    let gCheckBox = document.querySelector(".g-checkbox");
    mlCheckBox.addEventListener("change", function() {
        if (mlCheckBox.checked) {
            gCheckBox.checked = false;
        }
    });
    
    gCheckBox.addEventListener("change", function() {
        if (gCheckBox.checked) {
            mlCheckBox.checked = false;
        }
    });
}

let btnAddOC = () => {
    let oc = document.querySelector(".oc_solicitada").value;
    let qnt_solicitada = document.querySelector(".qnt_solicitada").value;
    let listaOCs = document.querySelector(".listaOCs");
    let contadorOCs = document.querySelector(".contadorOCs");
    
    let ocIndex = ocsAdded.findIndex(item => item.oc === oc);
    if (ocIndex === -1) {
        ocsAdded.push({
            oc: oc,
            qnt_solicitada: qnt_solicitada
        });
        
        listaOCs.innerHTML += `
        <tr>
            <td>${oc}</td>
            <td>${qnt_solicitada}</td>
        </tr>
        `
        contadorOCs.innerHTML = '';
        contadorOCs.innerHTML += `<h3>Quantidade adicionada: ${listaOCs.rows.length - 1}</h3>`
    }else{
        alert("OC já adicionada");
    }
    
    document.querySelector(".oc_solicitada").value = '';
    document.querySelector(".qnt_solicitada").value = '';
}


let renderizarForm40 = () => {
    let conteudo = document.querySelector(".conteudo");
    conteudo.innerHTML = '';
    conteudo.innerHTML += "Form 40";
}

let renderizarForm161 = () => {
    let conteudo = document.querySelector(".conteudo");
    conteudo.innerHTML = '';
    conteudo.innerHTML += "Form 161";
}

// Inicializando algumas funções
renderizarLogin();
