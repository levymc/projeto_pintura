// Variáveis Globais
const data = new Date();
const dia = String(data.getDate()).padStart(2, '0');
const mes = String(data.getMonth() + 1).padStart(2, '0');
const ano = data.getFullYear();
let dataAtual = dia + '/' + mes + '/' + ano;

let statusForm173 = 0;
let container = document.querySelector(".container");
let main = document.querySelector("main");
let user ;
let ocsAdded = [];
let dadosQuadros = [];
let impressora ;
let quadrosAdicionados = [] ;


// Modal de Erros Gerais
function erro(){
    Swal.fire({
        title: "Ocorreu um erro no sistema.",
        icon: "error"
    })
}

function sucesso(){
    Swal.fire({
        title: "Informações Enviadas com Sucesso!",
        icon: "success"
    })
}

// Definição de Eventos
document.querySelector(".titulo h1").addEventListener("click", function(){
    window.location.reload();
});

let enterKeyHandler = function(event) {
    if (event.key === "Enter") {
        acessoUserForm();
    }
};

function defImpressora(){
    listaSuspensa = document.querySelector('.defImpressora select')
    listaSuspensa.addEventListener('change', function() {
        const valorSelecionado = listaSuspensa.value;
    
        if (valorSelecionado === 'pcp') {
            console.log("pcp")
            impressora = 'RICOH MP C2504ex PCL 6';
        } else if (valorSelecionado === 'pintura') {
            impressora = 'RICOH Aficio SP 3510DN PCL 6';
            console.log("pintura")
        }else if (valorSelecionado === `dev`) {
            impressora = 'Microsoft Print to PDF'
            console.log('dev')
        }
    });
}




// Login
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



// Main
let renderizarMain = () => {
    container.innerHTML = '';
    container.innerHTML += `
            <div class="conteudo">
                <div class="kaban">
                    <div class="topo">
                        <button class="waves-effect waves-light btn-small red lighten-2" id="novaSolicitacao">Solicitar Nova Mescla</button> 
                        <section class="btnNewCEMB"><button id="btnNewCEMB" class="waves-effect waves-light btn-flat red lighten-2">Nova CEMB</button></section>
                        <section class="defImpressora">
                            <select name="defImpressora">
                                <option value="pintura" selected>Escolha a impressora</option>
                                <option value="pintura">Pintura</option>
                                <option value="pcp">PCP</option>
                                <option value="dev">Dev</option>
                            </select>
                        </section>
                    </div>
                    <div class="quadros-kanban">
                        Ainda não existem solicitações!
                    </div>
                </div>
            </div>
    `
    document.getElementById("novaSolicitacao").addEventListener("click", function(){
        modalSolicitacao();
    })
    document.getElementById("btnNewCEMB").addEventListener("click", function(){
        recebAllInfos();
    })
    carregarDadosQuadros()
    defImpressora();
}


// Modal Nova CEMB
function confereMEP(){
}

function recebAllInfos(){
    try{
        axios.get("/allInfoCEMB").then(response => {
            modalNewCEMB(response.data)
        }).catch(error => {
            erro();
            console.log(error);
        })
    }catch{
        erro();
    }
}

function modalNewCEMB(allInfoCEMB){
    let selected;
    let meps = []
    allInfoCEMB.map((info, i) => !meps.includes(info.norma.replace(/MEP/g, '').trim()) && meps.push(info.norma.replace(/MEP/g, '').trim()))

    const optionMeps = `
        ${meps.map((mep, i) => `<option value="${mep}">${mep}</option>`).join('\n')}
    `;
    console.log(meps)

    const html = `
    <div id="modalNewCEMB">
        <div class="flex input-field col s6">
            <label for="newCEMB">Novo Código EMBRAER</label>
            <input type="number" class="validate" name="newCEMB" id="newCEMB">
        </div>  
        <div class="flex input-field col s6">
            <label for="newCEMB">Descrição</label>
            <input type="text" class="validate" name="newDescription" id="newDescription">
        </div>  
        <div class="newMEP flex input-field col s6">
            <select id="newMEP" name="newMEP">
                <option value="" selected>Selecione a MEP</option>
                ${optionMeps}
                <option value="new" >Nova MEP</option>
            </select>
        </div>  
    </div>  
    `;
    Swal.fire({
        title:"Adicionar Nova Tinta",
        width: '40%',
        confirmButtonColor:"#b80000",
        confirmButtonText:"Adicionar",
        cancelButtonText:"Cancelar",
        allowOutsideClick: false,
        showCloseButton: true,
        showCancelButton: true,
        html: html,
        preConfirm: () => {
            const newCEMB = document.getElementById('newCEMB').value;
            const newMEP = document.getElementById('newMEP').value;
            const newDescription = document.getElementById('newDescription').value;
            if (!newCEMB || !newMEP || !newDescription) {
                Swal.showValidationMessage(`Todos os campos devem ser preenchidos corretamente.`)
            }else if (selected === "new"){
                const newMEP_adicionar = document.getElementById('newMEP_adicionar').value;
                const imageProp = document.getElementById('imageProp').value;
                if (!newMEP_adicionar || !imageProp ) {
                    Swal.showValidationMessage(`Todos os campos devem ser preenchidos corretamente.`)
                } else if (meps.includes(newMEP_adicionar.replace(/MEP/g, '').trim())){
                    Swal.showValidationMessage(`A MEP adicionada já existe!`)
                }
            }
            }
    }).then(response => {
        if( response.isConfirmed ){
            const dados ={
                newCEMB: document.getElementById('newCEMB').value,
                newMEP: document.getElementById('newMEP').value,
                newDescription: document.getElementById('newDescription').value,
            }
            if (selected === "new"){
                dados.newMEP_adicionar = document.getElementById('newMEP_adicionar').value;
                dados.imageProp = document.getElementById('imageProp').value;
            }
            console.log(dados)
            insertDB_newMEP(dados);
            
        }
    })

    document.getElementById("newMEP").addEventListener("change", function (){
        selected = this.value
        novaMEP(selected)
    })
}

function insertDB_newMEP(dados){
    try{
        axios.post("/newMEP", dados).then(response => {
            console.log(response)
            sucesso();
        }).catch(error => {
            console.log(error)
        })
    }catch(e){
        console.log(e)
    }
}

function novaMEP(valor){
    const modalNewCEMB = document.getElementById("modalNewCEMB");

    if (valor === "new"){
        !document.getElementById("newInput") ? modalNewCEMB.insertAdjacentHTML('beforeend', `
            <div id="newInput" class="flex input-field col s6">
                <label for="newMEP_adicionar">Nova MEP</label>
                <input type="text" class="validate" name="newMEP_adicionar" id="newMEP_adicionar">
            </div>  
            <div id="imageInput" class="file-field input-field">
                <div class="btn">
                    <span>Imagem Proporção de Mistura</span>
                    <input type="file" id="imageProp" name="myImage" accept="image/*">
                </div>
                <div class="file-path-wrapper">
                    <input class="file-path validate" type="text">
                </div>
            </div>  
        `) : document.getElementById("newInput").remove()
    }else{
        document.getElementById("newInput") && document.getElementById("newInput").remove()
    }
}


// Modal Form173
function modalSolicitacao(){
    Swal.fire({
    title:"Formulário 173 - Solicitação de Preparação de Tinta",
    width: '50%',
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
            <div class="numeroForm flex input-field col s6">
                <input type="number" class="validate" name="numeroForm" id="numeroForm">
                <label for="numeroForm">Formulário Nº</label>
            </div>
            <div class="codPintor flex input-field col s6"">
                <input class="validate" type="number" name="codPintor" id="codPintor">
                <label for="codPintor">Código do Pintor</label>
            </div>
            <div class="cemb flex input-field col s6"">
                <input class="validate" type="number" name="cemb" id="cemb">
                <label for="cemb">CEMB</label>
            </div>
            <div class="quantidade flex input-field col s6"">
                <input class="validate" type="number" name="quantidade" id="quantidade">
                <label for="quantidade">Quantidade Solicitada</label>
            </div>
            <div class="container-checkboxes flex">
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
        <div class="ocsForm173 divisoria-vertical">
            <div class="campoOC">
                <div class="input-field col s6"">
                    <input type="number" name="ocForm173" id="ocForm173" class="validate oc_solicitada">
                    <label for="ocForm173">OC</label>
                </div>
                <div class="input-field col s6"">
                    <input type="number" name="qntOcForm173" id="qntOcForm173" class="validate qnt_solicitada">
                    <label for="qntOcForm173">QNT</label>
                </div>
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
            } else if (g.checked === ml.checked) {
            Swal.showValidationMessage(`Selecione apenas uma opção entre "ml" e "g".`)
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
    console.log(ocsAdded)
    return ocsAdded
}



// Renderização dos Quadros no Kanban
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

function primeiroQuadro(){
    const dados = {
        numeroForm: document.querySelector(".numeroForm input").value,
        solicitante: user,
        codPintor: document.querySelector(".codPintor input").value,
        cemb: document.querySelector(".cemb input").value,
        quantidade: document.querySelector(".quantidade input").value,
        unidade: getUnidade(),
        ocs: ocsAdded,
        data: dataAtual,
        status: 0, // por padrão é 0, ou seja, ainda esta como pendente
    }
    //Enviar para o DB table form173 e ocs
    axios.post("/form173_inserir", dados).then(response =>{ //form 173
        dados.id = response.data.obj.id;
        console.log(response.data)
        axios.post("/ocs_inserir", {ocs: dados.ocs, id_form173: dados.id}).then(responseOCs => { //Ocs
            console.log(responseOCs);
            carregarDadosQuadros()
        })
    });
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
  
    axios.get("/dadosQuadrosHoje", {
      params: {
        status: statusForm173,
        data: dataAtual
      }
    }).then(response => {
      console.log(response.data);
      response.data.forEach(dado => {
        addQuadro(Object(dado));
      });
    });
}

function addQuadro(dados) {
    let quadros = document.querySelector(".quadros-kanban");
    let Ocs = [];

    quadrosAdicionados.push({id: dados.id, dados: dados})
    console.log(dados.ocs)
    dados.ocs.map((oc) =>
      oc.oc && Ocs.push(`
        <tr>
            <td>${oc.oc}</td>
            <td>${oc.quantidade}</td>
        </tr>
    `));

    let objDados = {
        cemb: dados.cemb, 
        mescla: dados.mescla,
        codPintor: dados.codPintor, 
        data: dados.data, id: dados.id,
        numeroForm: dados.numeroForm, 
        ocs: dados.ocs, 
        quantidade: dados.quantidade, 
        solicitante: dados.solicitante, 
        status: dados.status, 
        unidade: dados.unidade
    }
    let contador = quadros.children.length + 1;
    quadros.innerHTML += `
      <div class="quadro shadow-drop-center">
        <div class="quadro-contador">${contador}ª Solicitação</div>
        <div class="quadro-data">${dados.data}</div>
        <ul>
          <li>Número do Formulário: <b>${dados.numeroForm}</b></li>
          <li>Código do Pintor: <b>${dados.codPintor}</b></li>
          <li>Cemb: <b onclick="recebeInfosCEMB(${dados.cemb})" id="infosCEMB"><u>${dados.cemb}</u></b></li>
          <li>Quantidade Solicitada: <b>${dados.quantidade} ${dados.unidade}</b></li>
        </ul>
        <div class="quadro-btns">
          <button id="quadro-btnForm40" onclick="btnForm40(${dados.id})" >Form. 40: Preparação</button>
          <button id="quadro-btnFinalizar" onclick="btnFinalizar(${dados.id})">Finalizar</button>
        </div>
        <div class="quadro-btns">
            <button id="quadro-btnPrint" onclick="btnPrint(${dados.id}, '${user}')" >Form. 161: Imprimir/Salvar</button>
            <button id="quadro-btnEditar" onclick="btnEditar(${dados.id})">Ver OCs</button>
        </div>
      </div>`;
  
    ocsAdded = [];

}
  

// Especificações do CEMB
function recebeInfosCEMB(cemb){
    axios.post("/infosCEMB", {cemb: cemb}).then(response => {
        if(response.data.length > 0){
            console.log(response.data[0])
            infosCEMB(response.data[0])
        }else{
            erro()
        }
        
    }).catch(error => {
        console.log(error)
        erro()
    })
}

function infosCEMB(infos){
    let listaHTML = '<ul>\n';
    const nAparece = ['cemb', 'bico', 'flash_off', 'graph', 'temperatura_secagem', 'viscosimetro']
    for (const chave in infos) {
        if (infos.hasOwnProperty(chave) && !nAparece.includes(chave)) {
            if (chave == 'pot_life'){
                listaHTML += `  <li><b>${chave}</b>: ${infos[chave]} horas</li>\n`;
            }else{
                listaHTML += `  <li><b>${chave}</b>: ${infos[chave]}</li>\n`;
            }
        }
    }
    listaHTML += '</ul>';

    let html = `
        <div class="containerInfosCEMB">
            <div class="colunaEspecificacoes">
                <h5>Especificações</h5>
                ${listaHTML}
            </div>
            <div class="colunaParametros">
                <h5>Parâmetros</h5>
                <img class="graphProp" src="${infos.graph}" alt="Proporção" />
            </div>
        </div>
    `
    // Obtenha o elemento body
    const body = document.querySelector('body');
    const originalOverflowY = body.style.overflowY;
    body.style.overflowY = 'hidden';
    
    Swal.fire({
        title: `Especificações do CEMB <b>${infos.cemb}</b>`,
        icon: "info",
        width: '60%',
        confirmButtonColor: "#E57373",
        html: html,
        onClose: () => {
            body.style.overflowX = originalOverflowY;
        },
    })
}


// Editar OCs
function btnEditar(id){
    axios.get("/dadosQuadroId", {
        params: {
          id: id,
        }
        }).then(result => {
            axios.get("/dadosOcsId", {
                params: {
                    track_form173: id,
                }
                }).then(resultOC => {
                    modalEditarOCs(result.data ,resultOC.data)
                })
        })  
}


function modalEditarOCs(dadosQuadro, dadosOCs){
    let Ocs = [];
    let ocsAdicionadas = [];
    console.log(dadosQuadro, dadosOCs)
    dadosOCs.map((oc) =>
      oc.oc && Ocs.push(`
        <tr id="${oc.id}">
            <td>${oc.oc}</td>
            <td>${oc.quantidade}</td>
        </tr>
    `)
    );
    const html = `
        <div class="modalEditarOCs">
            <div class="inputsModalEditar flex ">
                <div class="divEditar flex input-field col s6">
                    <label for="ocsEditar">OCs</label>
                    <input type="number" class="validate" name="ocsEditar" id="ocsEditar">
                </div>
                <div class="divEditar flex input-field col s6">
                    <label for="qntEditar">Quantidade</label>
                    <input type="number" class="validate" name="qntEditar" id="qntEditar">
                </div>
            </div>
            <div class="tabelaEditar">
                <table class="responsive-table centered" >
                    <thead>
                    <tr>
                        <th>OCs</th>
                        <th>Quantidade</th>
                    </tr>
                    </thead>

                    <tbody>
                        ${Ocs.join('')}
                    </tbody>
                </table>
            </div>
            <section class="btnApagar" ><ion-icon id="btnApagar" name="trash-bin-outline"></ion-icon></section>
            <section class="btnAddOC_Editar"><ion-icon id="btnAddOC_Editar" name="add-outline"></ion-icon></section>
        </div>
    `
    Swal.fire({
        title: `Editar OCs - Id: ${dadosQuadro[0].id}`,
        confirmButtonColor: "#E57373",
        html: html,
        showCancelButton: true,
        cancelButtonText: "Cancelar",
        confirmButtonText: "Finalizar",
        allowOutsideClick: false,
        showConfirmButton: true,
    }).then(result => {
        if(result.isConfirmed && ocsAdicionadas.length != 0){
            console.log(ocsAdicionadas)
            carregarDadosQuadros();
        }
    })

    document.getElementById("btnAddOC_Editar").addEventListener("click", function(){
        insertOC_DB(dadosQuadro[0].id, ocsAdicionadas);
    })
    selecionarLinha()   
}


function selecionarLinha(){
    const linhasTabela = document.querySelectorAll('.tabelaEditar table tbody tr');
    linhasTabela.forEach(linha => {
        linha.addEventListener('click', () => {
            const estaSelecionada = linha.classList.contains('linha-selecionada'); // Verifica se a linha já está selecionada
            linhasTabela.forEach(linha => { // Remove a classe de seleção de todas as linhas
                linha.classList.remove('linha-selecionada');
            });
            
            if (estaSelecionada) { // Se a linha já estiver selecionada, desseleciona-a
                console.log('Linha desselecionada:', linha);
            }
            // Caso contrário, seleciona-a
            else {
                linha.classList.add('linha-selecionada');
                console.log('Linha selecionada:', linha);
                document.getElementById("btnApagar").addEventListener("click", function(){
                    if (confirm("Deseja apagar a OC?")){
                        linha.remove()
                        btnApagar(linha.id)
                    }
                })
            }
            });
        });
}


function btnApagar(idOC){
    console.log(idOC)
    axios.post("ocs_remove", {idOC: idOC}).then(result => {
        console.log(result)
        alert("OC removida com sucesso!")
    }).catch(error => {
        alert("Algum erro ocorreu")
        console.log(error)
    })
}


function insertOC_DB(id_form173, ocsAdicionadas){
    const ocsInput = document.getElementById("ocsEditar").value;
    const qntInput = document.getElementById("qntEditar").value;

    if (ocsInput && qntInput) {
        console.log(ocsInput, qntInput)
        axios.post("/ocs_inserir", {id_form173: id_form173, ocs: [{
            oc: ocsInput, 
            qnt_solicitada: qntInput
        }]}).then(response => {
            btnAddOC_Editar(ocsAdicionadas);
        }).catch(error => {
            alert("Ocorreu um erro no sistema.")
            console.log(error)
        })
    }else{
        Swal.showValidationMessage("Todos os campos devem ser preenchidos corretamente.");
    }
}

function btnAddOC_Editar(ocsAdicionadas){
    const ocsInput = document.getElementById("ocsEditar").value;
    const qntInput = document.getElementById("qntEditar").value;

    if (ocsInput && qntInput) {
        const novaLinha = `
            <tr>
                <td>${ocsInput}</td>
                <td>${qntInput}</td>
            </tr>
        `;
        const tabelaEditar = document.querySelector(".tabelaEditar tbody");
        tabelaEditar.insertAdjacentHTML("beforeend", novaLinha);
        
        // Limpar os inputs
        document.getElementById("ocsEditar").value = "";
        document.getElementById("qntEditar").value = "";
        
        ocsAdicionadas.push({ ocs: ocsInput, quantidade: qntInput });
        selecionarLinha();
    } else {
        alert("Preencha os campos para adicionar.")
    }
}



//Imprimir o Form 161
function btnPrint(id, user){
    Swal.fire({
        title: `Confirma a impressão - Id: ${id}`,
        icon: "question",
        confirmButtonColor: "#E57373",
        // html: html,
        showCancelButton: true,
        cancelButtonText: "Cancelar",
        confirmButtonText: "Sim",
        showConfirmButton: true,
    }).then(result => {
        if (result.isConfirmed){
            axios.post("/print161", {id: id, user: user, impressora: impressora})
        }else{
            console.log("Não")
        }
    })
}

// Modal Form40

function btnForm40(id) {
    let idQuadro = id

    const clearFormInputs = (idQuadro) => {
        localStorage.removeItem(`form40_temperatura_${idQuadro}`);
        localStorage.removeItem(`form40_umidade_${idQuadro}`);
        localStorage.removeItem(`form40_lotemp_${idQuadro}`);
        localStorage.removeItem(`form40_shelf_life_${idQuadro}`);
        localStorage.removeItem(`form40_viscosimetro_${idQuadro}`);
        localStorage.removeItem(`form40_viscosidade_${idQuadro}`);
        localStorage.removeItem(`form40_proporcao_${idQuadro}`);
        localStorage.removeItem(`form40_ini_agitador_${idQuadro}`);
        localStorage.removeItem(`form40_ini_mistura_${idQuadro}`);
        localStorage.removeItem(`form40_ini_diluentes_${idQuadro}`);
        localStorage.removeItem(`form40_ini_inducao_${idQuadro}`);
        localStorage.removeItem(`form40_ini_adequacao_${idQuadro}`);
      };
      

    const limparInputs = (idQuadro) => {
        document.getElementById('temperatura').value = "";
        document.getElementById('umidade').value = "";
        document.getElementById('lotemp').value = "";
        document.getElementById('shelf_life').value = "";
        document.getElementById('viscosimetro').value = "";
        document.getElementById('viscosidade').value = "";
        document.getElementById('proporcao').value = "";
        document.getElementById('ini_agitador').value = "";
        document.getElementById('ini_mistura').value = "";
        document.getElementById('ini_diluentes').value = "";
        document.getElementById('ini_inducao').value = "";
        document.getElementById('ini_adequacao').value = "";
    }

    function limparDois(idQuadro) {
        limparInputs(idQuadro);
        clearFormInputs(idQuadro);
    }

    const restoreFormInputs = (idQuadro) => {
        // Restaurar as informações do localStorage
        const temperatura = localStorage.getItem(`form40_temperatura_${idQuadro}`);
        const umidade = localStorage.getItem(`form40_umidade_${idQuadro}`);
        const lotemp = localStorage.getItem(`form40_lotemp_${idQuadro}`);
        const shelf_life = localStorage.getItem(`form40_shelf_life_${idQuadro}`);
        const viscosimetro = localStorage.getItem(`form40_viscosimetro_${idQuadro}`);
        const viscosidade = localStorage.getItem(`form40_viscosidade_${idQuadro}`);
        const proporcao = localStorage.getItem(`form40_proporcao_${idQuadro}`);
        const ini_agitador = localStorage.getItem(`form40_ini_agitador_${idQuadro}`);
        const ini_mistura = localStorage.getItem(`form40_ini_mistura_${idQuadro}`);
        const ini_diluentes = localStorage.getItem(`form40_ini_diluentes_${idQuadro}`);
        const ini_inducao = localStorage.getItem(`form40_ini_inducao_${idQuadro}`);
        const ini_adequacao = localStorage.getItem(`form40_ini_adequacao_${idQuadro}`);
  
        // Preencha os campos com as informações restauradas
        const modalElement = document.querySelector('.modalForm40');
        if (modalElement) {
            document.getElementById('temperatura').value = temperatura;
            document.getElementById('umidade').value = umidade;
            document.getElementById('lotemp').value = lotemp;
            document.getElementById('shelf_life').value = shelf_life;
            document.getElementById('viscosimetro').value = viscosimetro;
            document.getElementById('viscosidade').value = viscosidade;
            document.getElementById('proporcao').value = proporcao;
            document.getElementById('ini_agitador').value = ini_agitador;
            document.getElementById('ini_mistura').value = ini_mistura;
            document.getElementById('ini_diluentes').value = ini_diluentes;
            document.getElementById('ini_inducao').value = ini_inducao;
            document.getElementById('ini_adequacao').value = ini_adequacao;
        }   
      };
  
      const saveFormInputs = (idQuadro) => {
        // Salvar as informações no localStorage
        localStorage.setItem(`form40_temperatura_${idQuadro}`, document.getElementById(`temperatura`).value);
        localStorage.setItem(`form40_umidade_${idQuadro}`, document.getElementById(`umidade`).value);
        localStorage.setItem(`form40_lotemp_${idQuadro}`, document.getElementById(`lotemp`).value);
        localStorage.setItem(`form40_shelf_life_${idQuadro}`, document.getElementById(`shelf_life`).value);
        localStorage.setItem(`form40_viscosimetro_${idQuadro}`, document.getElementById(`viscosimetro`).value);
        localStorage.setItem(`form40_viscosidade_${idQuadro}`, document.getElementById(`viscosidade`).value);
        localStorage.setItem(`form40_proporcao_${idQuadro}`, document.getElementById(`proporcao`).value);
        localStorage.setItem(`form40_ini_agitador_${idQuadro}`, document.getElementById(`ini_agitador`).value);
        localStorage.setItem(`form40_ini_mistura_${idQuadro}`, document.getElementById(`ini_mistura`).value);
        localStorage.setItem(`form40_ini_diluentes_${idQuadro}`, document.getElementById(`ini_diluentes`).value);
        localStorage.setItem(`form40_ini_inducao_${idQuadro}`, document.getElementById(`ini_inducao`).value);
        localStorage.setItem(`form40_ini_adequacao_${idQuadro}`, document.getElementById(`ini_adequacao`).value);
      };
    axios.get("/dadosQuadroId", {
        params: {
          id: id,
        }
      }).then(response => {
        console.log(response.data[0]);
        restoreFormInputs(idQuadro);
        axios.get("/viscosimetro", {
            params: {
                cemb: response.data[0].cemb
            }
        }).then(tinta => {
            console.log(tinta.data)
            const viscosimetro = `${tinta.data.map((copo, i) => 
                `<option value="${copo}">${copo}</option>`
            )}
            `;
            console.log(viscosimetro)       
            
            const html = `
            <div class="modalForm40">
                <div class="coluna1">
                    <div class="responsavel"> Preparador: <b>${user}</b></div>
                    <div class="mescla"> Mescla: <b>${response.data[0].mescla}</b></div>
                    <div class="dataForm40"> Data: <b>${dataAtual}</b></div>
                    <div class="cemb"> CEMB Solicitada: <b>${response.data[0].cemb}</b></div>
                    <div class="qnt_solicitada"> Quantidade: <b>${String(response.data[0].quantidade)+response.data[0].unidade}</b></div>
                </div>
                <div class="coluna2">
                    <div class="temperatura">
                        <input type="number" id="temperatura" placeholder="Temperatura">
                    </div>
                    <div class="umidade">
                        <input type="number" id="umidade" placeholder="Umidade">
                    </div>
                    <div class="lotemp">
                        <input type="text" id="lotemp" placeholder="Lote da Matéria Prima">
                    </div>
                    <div class="shelf_life">
                        <input type="number" id="shelf_life" placeholder="Shelf Life">
                    </div>
                    <div class="viscosimetro newMEP flex input-field col s6">
                        <select id="viscosimetro" name="newMEP">
                            <option value="" selected>Selecione o Viscosímetro</option>
                            ${viscosimetro}
                        </select>
                    </div>
                    <div class="viscosidade">
                        <input type="number" id="viscosidade" placeholder="Viscosidade">
                    </div>
                    <div class="proporcao">
                        <input type="text" id="proporcao" placeholder="Proporção">
                    </div>
                    <div class="pot_life">
                        <input type="text" id="pot_life" placeholder="Pot Life">
                    </div>
                </div>
                <div class="colunaTempos">
                    <div class="ini_agitador">
                        <label for="ini_agitador">Início Agitador</label>
                        <input type="time" min="07:00" max="17:20" name="ini_agitador" id="ini_agitador">
                    </div>
                    <div class="ini_mistura">
                        <label for="ini_mistura">Início Mistura</label>
                        <input type="time" min="07:00" max="17:20" name="ini_mistura" id="ini_mistura"">
                    </div>
                    <div class="ini_diluentes">
                        <label for="ini_diluentes">Início Diluentes</label>
                        <input type="time" min="07:00" max="17:20" name="ini_diluentes" id="ini_diluentes">
                    </div>
                    <div class="ini_inducao">
                        <label for="ini_inducao">Início Indução</label>
                        <input type="time" min="07:00" max="17:20" name="ini_inducao" id="ini_inducao">
                    </div>
                    <div class="ini_adequacao">
                        <label for="ini_adequacao">Início Adequação</label>
                        <input type="time" min="07:00" max="17:20" name="ini_adequacao" id="ini_adequacao">
                    </div>
                </div>
                <section class="btnReset"><button id="btnReset">Limpar Dados</button></section>
                <section class="btnAutorizar"><button id="btnAutorizar">Excessão: Autorizar</button></section>
            </div>
            `
            
            Swal.fire({
                title: "Form. 40 - Preparação de Tinta",
                confirmButtonColor: "#E57373",
                html: html,
                width: '75%',
                showCancelButton: true,
                cancelButtonText: "Minimizar",
                confirmButtonText: "Enviar",
                showConfirmButton: true,
                // preConfirm: () => {
                //     dados = {
                            // track_form173: idQuadro,
                            // mescla: 1,
                            // data_prep: dataAtual,
                            // cod_mp: response.data[0].cemb,
                            // temperatura: document.getElementById(`temperatura`).value,
                            // umidade: document.getElementById(`umidade`).value,
                            // lotemp: document.getElementById(`lotemp`).value,
                            // shelf_life: document.getElementById(`shelf_life`).value,
                            // viscosimetro: document.getElementById(`viscosimetro`).value,
                            // viscosidade: document.getElementById(`viscosidade`).value,
                            // proporcao: document.getElementById(`proporcao`).value,
                            // responsavel: user,
                            // excessao: 0,
                            // pot_life: document.getElementById(`pot_life`).value,
                            // ini_agitador: document.getElementById(`ini_agitador`).value,
                            // ini_mistura: document.getElementById(`ini_mistura`).value,
                            // ini_diluentes: document.getElementById(`ini_diluentes`).value,
                            // ini_inducao: document.getElementById(`ini_inducao`).value,
                            // ini_adequacao: document.getElementById(`ini_adequacao`).value,
                //     }
                //     const hasZeroValue = Object.values(dados).some(value => value === '');
                //     if (hasZeroValue) {
                //     Swal.showValidationMessage("Todos os campos devem ser preenchidos corretamente.");
                //     }
                // }
                }).then((result) => {
                    dados = {
                        track_form173: idQuadro,
                        mescla: 1,
                        data_prep: dataAtual,
                        cod_mp: response.data[0].cemb,
                        temperatura: document.getElementById(`temperatura`).value,
                        umidade: document.getElementById(`umidade`).value,
                        lotemp: document.getElementById(`lotemp`).value,
                        shelf_life: document.getElementById(`shelf_life`).value,
                        viscosimetro: document.getElementById(`viscosimetro`).value,
                        viscosidade: document.getElementById(`viscosidade`).value,
                        proporcao: document.getElementById(`proporcao`).value,
                        responsavel: user,
                        excessao: 0,
                        pot_life: document.getElementById(`pot_life`).value,
                        ini_agitador: document.getElementById(`ini_agitador`).value,
                        ini_mistura: document.getElementById(`ini_mistura`).value,
                        ini_diluentes: document.getElementById(`ini_diluentes`).value,
                        ini_inducao: document.getElementById(`ini_inducao`).value,
                        ini_adequacao: document.getElementById(`ini_adequacao`).value,
                    }
                    
                    if (!result.isDismissed) {
                        axios.post("/form40_inserir", dados).then(response => {
                            console.log(response.data)
                        })
                    } else {
                    // O modal foi minimizado, salvar as informações no localStorage
                    saveFormInputs(idQuadro);
                    }
                });
                document.getElementById("btnReset").addEventListener("click", function(){
                    limparDois(idQuadro);
                })
                document.getElementById("btnAutorizar").addEventListener("click", function(){
                    saveFormInputs(idQuadro);
                    Swal.fire({
                        title: 'Login',
                        html: `
                            <div class="input-field">
                                <input id="username" type="text" class="validate">
                                <label for="username">Usuário</label>
                            </div>
                            <div class="input-field">
                                <input id="password" type="password" class="validate">
                                <label for="password">Senha</label>
                            </div>
                        `,
                        showCancelButton: true,
                        confirmButtonText: 'Acesso Processo',
                        preConfirm: () => {
                            const username = Swal.getPopup().querySelector('#username').value;
                            const password = Swal.getPopup().querySelector('#password').value;
                            // Aqui você pode fazer a validação do usuário e senha
                            axios.post("/acessoProcesso", {userInput: username, passInput: password}).then(result => {
                                console.log(result.data)
                                if(result.data.succes){
                                    console.log("success")
                                }
                            }).catch((e) => {
                                console.log(e)
                                Swal.showValidationMessage('Usuário ou senha incorretos');
                            })
                            
                            // if (acessoProcesso) {
                            //     return { username, password };
                            // } else {
                            //     Swal.showValidationMessage('Usuário ou senha incorretos');
                            //     return false;
                            // }
                        }
                    }).then((result) => {
                        if (result.isConfirmed) {
                            btnForm40(idQuadro);
                            const { username, password } = result.value;
                            // Aqui você pode fazer o processamento do login com os dados fornecidos
                            console.log('Usuário:', username);
                            console.log('Senha:', password);
                        }
                    });
                })
                restoreFormInputs(idQuadro);
            }).catch(e => {alert("Erro: ", e)})
            
            
        }
        
)}



// Finalização do Quadro no Kanban -> solicitação de tinta finalizada.
function btnFinalizar(id){
    console.log(id)
    Swal.fire({
        title:`Deseja finalizar a solicitação?`,
        icon:"question",
        showCancelButton: true,
        cancelButtonText: "Cancelar",
        confirmButtonText: "Sim!",
        confirmButtonColor: "#E57373",
    }).then(response => {
        if (response.isConfirmed){
            axios.post("/finalizarQuadro", {id:id}).then(res => {
                carregarDadosQuadros();
                console.log(res);
            })
        }
    })
}



// Inicializando algumas funções
renderizarLogin();
