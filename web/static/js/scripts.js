// Variáveis Globais
let container = document.querySelector(".container");
let main = document.querySelector("main");
let user ;
let ocsAdded = [];

document.querySelector(".titulo").addEventListener("click", function(){
    window.location.reload();
});

let enterKeyHandler = function(event) {
    if (event.key === "Enter") {
        acessoUserForm();
    }
};




let renderizarLogin = () => {
    container.innerHTML = '';
    container.innerHTML = `
    <div class="userForm flex ">
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
        // kaban();
    }).catch(error => {
        console.log(error);
        alert("Ocorreu algum erro, tente novamente ou acione o Processo.")
    })
}

let renderizarMain = () => {
    container.innerHTML = '';
    container.innerHTML += `
            <nav class="menu-superior">
                <a class="btn" id="btn-form173">Solicitação de Tinta</a>
                <a class="btn" id="btn-form40">Preparação da Tinta</a>
                <a class="btn" id="btn-form161">Aplicação da Tinta</a>
            </nav>
            <div class="conteudo">
                <div class="kaban">
                    <div class="topo"><button class="waves-effect waves-light btn-small red lighten-2" id="novaSolicitacao">Solicitar Nova Mescla</button></div>
                    <div class="quadros-kanban">
                        Ainda não existem solicitações!
                    </div>
                </div>
            </div>
    `
    document.getElementById("btn-form173").addEventListener("click", function(){
        renderizarForm173();
    });
    document.getElementById("btn-form40").addEventListener("click", function(){
        renderizarForm40();
    });
    document.getElementById("btn-form161").addEventListener("click", function(){
        renderizarForm161();
    });
    document.getElementById("novaSolicitacao").addEventListener("click", function(){
        modalSolicitacao();
    })
}

function modalSolicitacao(){
        Swal.fire({
        title:"Formulário 173 - Solicitação de Preparação de Tinta",
        width: '60%',
        confirmButtonColor:"#b80000",
        confirmButtonText:"Enviar",
        cancelButtonText:"Cancelar",
        allowOutsideClick: false,
        showCloseButton: true,
        showCancelButton: true,
        html: `
        <div class="conteudo-form173">
            <div class="form173">
                <div class="solicitante">
                    <h3>Solicitante: <b>${user}</b></h3>
                </div>
                <div class="numeroForm">
                    <input type="number" placeholder="Formulário Nº">
                </div>
                <div class="codPintor">
                    <input type="number" placeholder="Código do Pintor">
                </div>
                <div class="cemb">
                    <input type="number" placeholder="CEMB">
                </div>
                <div class="quantidade">
                    <input type="number" placeholder="Quantidade Solicitada">
                    <div class="container-checkboxes">
                        <div class="checkboxes">
                            <input type="checkbox" id="g" name='g' value="g">
                            <label for="g">g</label>
                        </div>
                        <div class="checkboxes">
                            <input type="checkbox" id="ml" name='ml' value="ml">
                            <label for="ml">ml</label>
                        </div>
                    </div>
                </div>
            </div>
            <div class="ocsForm173">
                <div class="campoOC">
                    <input type="number" placeholder="OC" class="oc_solicitada">
                    <input type="number" placeholder="Quantidade" class="qnt_solicitada">
                </div>
                <div class="btnAddOC"><button onclick="btnAddOC()">Adicionar OC</button></div>
                <div class="container-listaOCs">
                    <table class="listaOCs">
                        <tr>
                            <th>OC</th>
                            <th>Quantidade</th>
                        </tr>
                    </table>
                </div>
                <div class="contadorOCs"></div>
            </div>
        </div>
        `
    }).then(response => {
        if (response.isConfirmed){
            primeiroQuadro();
        }
    })
     // Obtém os elementos de checkbox
    const checkboxG = document.getElementById('g');
    const checkboxML = document.getElementById('ml');

    // Adiciona um evento de clique nos checkboxes
    checkboxG.addEventListener('click', () => {
    // Se o checkbox G for selecionado, desmarque o checkbox ML
    if (checkboxG.checked) {
        checkboxML.checked = false;
    }
    });

    checkboxML.addEventListener('click', () => {
    // Se o checkbox ML for selecionado, desmarque o checkbox G
    if (checkboxML.checked) {
        checkboxG.checked = false;
    }
    });
}

function primeiroQuadro(){
    const dados = {
        numeroForm: document.querySelector(".numeroForm input").value,
        codPintor: document.querySelector(".codPintor input").value,
        cemb: document.querySelector(".cemb input").value,
        quantidade: document.querySelector(".quantidade input").value,
        unidade: getUnidade(),
        ocs: ocsAdded,
    };
    if(document.querySelector(".quadro")){
        addQuadro(dados);
    }else{
        let quadros = document.querySelector(".quadros-kanban");
        quadros.innerHTML = '';
        addQuadro(dados);
    }
}

function getUnidade() {
  var checkboxML = document.getElementById("ml");
  var checkboxG = document.getElementById("g");
  var unidade = "";

  if (checkboxML.checked) {
    unidade = checkboxML.value;
  } else if (checkboxG.checked) {
    unidade = checkboxG.value;
  }

  return unidade;
}


function addQuadro(dados){
    // ELe vai ter que buscar no servidor pelas solicitações ainda pendentes e trazer todas elas de novo......
    let quadros = document.querySelector(".quadros-kanban");
    // conteudo.innerHTML = '';
    let Ocs = []
    dados.ocs.map((oc) => 
        Ocs.push(`<li>${oc.oc}</li>`)
        )
    quadros.innerHTML += `
    <div class="quadro">
        <ul>
            <li>Número do Formulário: ${dados.numeroForm}</li>
            <li>Código do Pintor: ${dados.codPintor}</li>
            <li>Cemb: ${dados.cemb}</li>
            <li>Quantidade Solicitada: ${dados.quantidade} ${dados.unidade}</li>
        </ul>
        <div class="ocsQuadro"> 
            OCs:
            <ul>
                ${Ocs}
            </ul>
        </div> 

    </div>`; // Na hora que adicionar
    ocsAdded = [];
}

function kaban() {
    // let conteudo = document.querySelector(".conteudo");
    container.innerHTML = '';
    container.innerHTML += `
        <div class="kaban">
            <div class="topo"><button>+ Solicitar Nova Mescla</button></div>
            <div class="quadros-kanban">
            </div>
        </div>
    `
}

var renderizarForm173 = () => {
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
    conteudo.innerHTML += "<div class='conteudo-form40'>Form 40</div>";
}

let renderizarForm161 = () => {
    let conteudo = document.querySelector(".conteudo");
    conteudo.innerHTML = '';
    conteudo.innerHTML += "Form 161";
}

// Inicializando algumas funções
renderizarLogin();
