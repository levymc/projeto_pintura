

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
            <div class="conteudo">
                <div class="kaban">
                    <div class="topo"><button class="waves-effect waves-light btn-small red lighten-2" id="novaSolicitacao">Solicitar Nova Mescla</button></div>
                    <div class="quadros-kanban">
                        Ainda não existem solicitações!
                    </div>
                </div>
            </div>
    `
    document.getElementById("novaSolicitacao").addEventListener("click", function(){
        modalSolicitacao();
    })
    carregarDadosQuadros()

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
  
    dados.ocs.map((oc) =>
      oc.oc ? Ocs.push(`<li>${oc.oc}</li>`) : Ocs.push(`<li>Sem OCs adicionadas</li>`)
    );

    const objDados = {
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
    console.log(objDados)

    let contador = quadros.children.length + 1;
  
    quadros.innerHTML += `
      <div class="quadro shadow-drop-center">
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
            ${Ocs.join('')}
          </ul>
        </div> 
        <div class="quadro-btns">
          <button id="quadro-btnForm40" onclick="btnForm40(${dados.id})" >Form. 40</button>
          <button id="quadro-btnFinalizar" onclick="btnFinalizar(${contador})">Finalizar</button>
        </div>
      </div>`;
  
    ocsAdded = [];
  }
  
  function btnForm40(id) {
    const restoreFormInputs = () => {
        // Restaurar as informações do localStorage
        const temperatura = localStorage.getItem('form40_temperatura');
        const umidade = localStorage.getItem('form40_umidade');
        const lotemp = localStorage.getItem('form40_lotemp');
        const shelflife = localStorage.getItem('form40_shelflife');
        const viscosimetro = localStorage.getItem('form40_viscosimetro');
        const viscosidade = localStorage.getItem('form40_viscosidade');
        const proporcao = localStorage.getItem('form40_proporcao');
        const ini_agitador = localStorage.getItem('form40_ini_agitador');
        const ini_mistura = localStorage.getItem('form40_ini_mistura');
        const ini_diluentes = localStorage.getItem('form40_ini_diluentes');
        const ini_inducao = localStorage.getItem('form40_ini_inducao');
        const ini_adequacao = localStorage.getItem('form40_ini_adequacao');
  
        // Preencha os campos com as informações restauradas
        const modalElement = document.querySelector('.modalForm40');
        if (modalElement) {
            document.getElementById('temperatura').value = temperatura;
            document.getElementById('umidade').value = umidade;
            document.getElementById('lotemp').value = lotemp;
            document.getElementById('shelflife').value = shelflife;
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
  
      const saveFormInputs = () => {
        // Salvar as informações no localStorage
        console.log(document.getElementById('temperatura').value)
        localStorage.setItem('form40_temperatura', document.getElementById('temperatura').value);
        localStorage.setItem('form40_umidade', document.getElementById('umidade').value);
        localStorage.setItem('form40_lotemp', document.getElementById('lotemp').value);
        localStorage.setItem('form40_shelflife', document.getElementById('shelflife').value);
        localStorage.setItem('form40_viscosimetro', document.getElementById('viscosimetro').value);
        localStorage.setItem('form40_viscosidade', document.getElementById('viscosidade').value);
        localStorage.setItem('form40_proporcao', document.getElementById('proporcao').value);
        localStorage.setItem('form40_ini_agitador', document.getElementById('ini_agitador').value);
        localStorage.setItem('form40_ini_mistura', document.getElementById('ini_mistura').value);
        localStorage.setItem('form40_ini_diluentes', document.getElementById('ini_diluentes').value);
        localStorage.setItem('form40_ini_inducao', document.getElementById('ini_inducao').value);
        localStorage.setItem('form40_ini_adequacao', document.getElementById('ini_adequacao').value);
      };
    axios.get("/dadosQuadroId", {
        params: {
          id: id,
        }
      }).then(response => {
        console.log(response.data[0]);
        restoreFormInputs();
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
                <div class="shelflife">
                    <input type="number" id="shelflife" placeholder="Shelf Life">
                </div>
                <div class="viscosimetro">
                    <input type="number" id="viscosimetro" placeholder="Viscosímetro">
                </div>
                <div class="viscosidade">
                    <input type="number" id="viscosidade" placeholder="Viscosidade">
                </div>
                <div class="proporcao">
                    <input type="text" id="proporcao" placeholder="Proporção">
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
        </div>
    `
    Swal.fire({
        title: "Form. 40 - Preparação de Tinta",
        confirmButtonColor: "#E57373",
        html: html,
        width: '75%',
        showCancelButton: true,
        showConfirmButton: true,
        }).then((result) => {
            if (!result.isDismissed) {
              // O modal foi fechado, então restaure os valores
              restoreFormInputs();
            } else {
              // O modal foi descartado, salvar as informações no localStorage
              saveFormInputs();
            }
          });
        }
    )}
    
  
  function minimizarModal() {
    Swal.getPopup().style.display = 'none';
    Swal.getContainer().style.pointerEvents = 'none';
    Swal.getTitle().style.display = 'none';
    Swal.getFooter().style.display = 'none';
  }
  
  

function btnFinalizar(solicitacao){
    console.log(solicitacao)
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
    console.log(ocsAdded)
    return ocsAdded
}

function btnRemoveOC(){
    console.log(ocsAdded)
}

// Inicializando algumas funções
renderizarLogin();
