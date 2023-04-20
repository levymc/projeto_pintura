// Variáveis Globais
let container = document.querySelector(".container");


let renderizarLogin = () => {
    container.innerHTML = '';
    
};

let acessoUserForm = () => {
    let userInput = document.querySelector(".userInput").value;
    let passInput = document.querySelector(".passInput").value;
    console.log(userInput);
    console.log(passInput);
    // aqui entra o axios para enviar o user e senha para conferir com o banco
}