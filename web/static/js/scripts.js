// Variáveis Globais

const data = new Date();
const dia = String(data.getDate()).padStart(2, '0');
const mes = String(data.getMonth() + 1).padStart(2, '0');
const ano = data.getFullYear();
let dataAtual = dia + '/' + mes + '/' + ano;


let container = document.querySelector(".container");
let main = document.querySelector("main");
let user ;
let ocsAdded = [];
let dadosQuadros = [];

document.querySelector(".titulo h1").addEventListener("click", function(){
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
        customClass: {
            validationMessage: 'my-validation-message'
          },
        html: `
        <div class="conteudo-form173">
            <div class="form173">
                <div class="solicitante">
                    <h3>Solicitante: <b>${user}</b></h3>
                </div>
                <div class="numeroForm">
                    <input type="number" id="numeroForm" placeholder="Formulário Nº">
                </div>
                <div class="codPintor">
                    <input type="number" id="codPintor" placeholder="Código do Pintor">
                </div>
                <div class="cemb">
                    <input type="number" id="cemb" placeholder="CEMB">
                </div>
                <div class="quantidade">
                    <input type="number" id="quantidade" placeholder="Quantidade Solicitada">
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
            <div class="ocsForm173 divisoria-vertical">
                <div class="campoOC">
                    <input type="number" id="ocForm173" placeholder="OC" class="oc_solicitada">
                    <input type="number" id="qntOcForm173" placeholder="Quantidade" class="qnt_solicitada">
                </div>
                <div class="btnAddOC">
                    <button class="display-none" id="btnRemoveOC" onclick="btnRemoveOC()">Remover OC</button>
                    <button id="btnAddOC" onclick="btnAddOC()">Adicionar OC</button>
                </div>
                <div class="container-listaOCs">
                    <table class="listaOCs text-center display-none">
                        <tr class="text-center">
                            <th>OC</th>
                            <th>Quantidade</th>
                        </tr>
                    </table>
                </div>
                <div class="contadorOCs"></div>
            </div>
        </div>
        `,
        preConfirm: () => {
            const numeroForm = document.getElementById('numeroForm').value;
            const codPintor = document.getElementById('codPintor').value;
            const cemb = document.getElementById('cemb').value;
            const quantidade = document.getElementById('quantidade').value;
            const g = document.getElementById('g');
            const ml = document.getElementById('ml');
        
            if (!numeroForm || !codPintor || !cemb || !quantidade || (!g.checked && !ml.checked) || (g.checked && ml.checked)) {
                Swal.showValidationMessage(`Todos os campos devem ser preenchidos corretamente.`)
                // setTimeout(() => {
                //   Swal.resetValidationError()
                // }, 5000) // tempo em milissegundos (5 segundos)
              } else if (g.checked === ml.checked) {
                Swal.showValidationMessage(`Selecione apenas uma opção entre "ml" e "g".`)
                // setTimeout(() => {
                //   Swal.resetValidationError()
                // }, 5000) // tempo em milissegundos (5 segundos)
              }
          }
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
        data: dataAtual,
    };
    dadosQuadros.push(dados);

    // Salvar no localStorage
    localStorage.setItem('dadosQuadros', JSON.stringify(dadosQuadros));

    if(document.querySelector(".quadro")){
        carregarDadosQuadros();
    }else{
        let quadros = document.querySelector(".quadros-kanban");
        quadros.innerHTML = '';
        carregarDadosQuadros();
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

function carregarDadosQuadros() {
    let quadros = document.querySelector(".quadros-kanban");
    quadros.innerHTML = '';
  
    // Verifica se há dados no localStorage
    if (localStorage.getItem('dadosQuadros')) {
      dadosQuadros = JSON.parse(localStorage.getItem('dadosQuadros'));
  
      // Adiciona os quadros a partir dos dados salvos
      dadosQuadros.forEach((dados) => {
        addQuadro(dados);
      });
    }
  }

  function addQuadro(dados) {
    let quadros = document.querySelector(".quadros-kanban");
    let Ocs = [];
  
    dados.ocs.map((oc) => Ocs.push(`<li>${oc.oc}</li>`));
  
    let contador = quadros.children.length + 1;
    dados.id = contador;

    quadros.innerHTML += `
      <div class="quadro">
          <div class="quadro-contador">${contador}ª Solicitação</div>
          <div class="quadro-data">${dados.data}</div>
          <ul>
              <li>Número do Formulário: <b>${dados.numeroForm}</b></li>
              <li>Código do Pintor: <b>${dados.codPintor}</b></li>
              <li>Cemb: <b>${dados.cemb}</b></li>
              <li>Quantidade Solicitada: <b>${dados.quantidade} ${dados.unidade}</b></li>
          </ul>
          <div class="ocsQuadro"> 
              OCs:
              <ul>
                  ${Ocs.join('')} <!-- Utilize o método join() sem o delimitador -->
              </ul>
          </div> 
          <div class="quadro-btns">
            <button id="quadro-btnForm40" onclick="btnForm40(${dados.id})">Form. 40</button>
            <button id="quadro-btnFinalizar" onclick="btnFinalizar(${contador})">Finalizar</button>
          </div>
      </div>`;
  
    ocsAdded = [];
  }
  
function btnForm40(id) {
    if (localStorage.getItem('dadosQuadros')) {
        dadosQuadros = JSON.parse(localStorage.getItem('dadosQuadros'));
    }

    console.log(dadosQuadros[0].numeroForm)

    let html = `
        <div class="container-Form40">
    `;

    for (let i = 0; i < dadosQuadros.length; i++) {
        console.log(dadosQuadros[i].id, id)
        if (dadosQuadros[i].id === id) {
        // Adicione aqui o conteúdo específico do objeto ao array html
        html += `<div>${dadosQuadros[i].numeroForm}</div></div>`;
        // Continue adicionando outros conteúdos necessários
        }
    }

    Swal.fire({
        title: "Form. 40 - Preparação de Tinta",
        confirmButtonColor: "#E57373",
        icon: "question",
        html: html, 
    });
}
  

function btnFinalizar(solicitacao){
    Swal.fire({
        title:`Deseja finalizar a ${solicitacao}ª solicitação?`,
        icon:"question",
        showCancelButton: true,
        cancelButtonText: "Cancelar",
        confirmButtonText: "Sim!",
        confirmButtonColor: "#E57373",
    })
}


function kaban() {
    // let conteudo = document.querySelector(".conteudo");
    container.innerHTML = '';
    container.innerHTML += `
        <div class="kaban">
            <div class="topo"><button>Solicitar Nova Mescla</button></div>
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
    const ocForm173 = document.getElementById('ocForm173').value;
    const qntOcForm173 = document.getElementById('qntOcForm173').value;
    if (!ocForm173 || !qntOcForm173){
        Swal.showValidationMessage(`Preencha os campos de OC e Quantidade.`);
    }else{
        let oc = document.querySelector(".oc_solicitada").value;
        let qnt_solicitada = document.querySelector(".qnt_solicitada").value;
        let listaOCs = document.querySelector(".listaOCs");
        let contadorOCs = document.querySelector(".contadorOCs");
        let btnRemoveOC = document.getElementById("btnRemoveOC");
        listaOCs.classList.remove("display-none");
        btnRemoveOC.classList.remove("display-none");
        
        
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
        const linhasTabela = document.querySelectorAll('.listaOCs td');

        // Adicione um evento de clique a cada linha
        linhasTabela.forEach(linha => {
            linha.addEventListener('click', () => {
                // Verifica se a linha já está selecionada
                const estaSelecionada = linha.classList.contains('linha-selecionada');
              
                // Remove a classe de seleção de todas as linhas
                linhasTabela.forEach(linha => {
                  linha.classList.remove('linha-selecionada');
                });
              
                // Se a linha já estiver selecionada, desseleciona-a
                if (estaSelecionada) {
                  console.log('Linha desselecionada:', linha);
                }
                // Caso contrário, seleciona-a
                else {
                  linha.classList.add('linha-selecionada');
                  console.log('Linha selecionada:', linha);
                }
              });
              
        });
    }
    
}

function btnRemoveOC(){
    
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
