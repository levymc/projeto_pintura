// Variáveis Globais
let container = document.querySelector(".container");


let renderizarLogin = () => {
    container.innerHTML = '';
    container.innerHTML = `
    <div class="userForm flex">
        <input class="userInput" name="userInput" type="text" placeholder="Usuário">
        <input class="passInput" name="passInput" type="text" placeholder="Senha">
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
        container.innerHTML = '';
    }).catch(error => {
        console.log(error);
        alert("Ocorreu algum erro, tente novamente ou acione o Processo.")
    })
}


// Inicializando algumas funções
renderizarLogin();