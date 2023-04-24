// Variáveis Globais
let container = document.querySelector(".container");
let user ;


let renderizarLogin = () => {
    container.innerHTML = '';
    container.innerHTML = `
    <div class="userForm flex">
        <input class="userInput" name="userInput" type="text" placeholder="Usuário">
        <input class="passInput" name="passInput" type="password" placeholder="Senha">
        <button onclick="acessoUserForm()" id="btn-userForm">Entrar</button>
    </div>`
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
                <button onclick="renderizarForm173()">Solicitar Tinta</button>
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
                <input type="text" placeholder="Código do Pintor">
            </div>
            <div class="cemb">
                <input type="text" placeholder="CEMB">
            </div>
            <div class="quantidade">
                <input type="text" placeholder="Quantidade Solicitada">
            </div>
        </div>
        <div class="ocsForm173">
            <div class="oc">
                <input type="text" placeholder="OC">
                <input type="text" placeholder="Quantidade">
            </div>
        </div>
    </div>
    `;
    
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