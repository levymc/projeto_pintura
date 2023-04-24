// Variáveis Globais
let container = document.querySelector(".container");


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
    conteudo.innerHTML += "Form 173";
    
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