
function formatar_datas_paciente(){
    formatarData2();
}

function formatarData2(event) {
    var campo = document.getElementById('id_data_nascimento');

    // Obtém o valor atual do campo
    var valor = campo.value;
    valor = valor.replace(/\s/g, '');

    // Verifica se a data está no formato "YYYY-mm-dd"
    var regex = /^\d{4}-\d{2}-\d{2}$/;
    if (regex.test(valor)) {
        // Formata a data para o formato "dd/mm/YYYY"
        var partes = valor.split('-');
        var novaData = partes[2] + '/' + partes[1] + '/' + partes[0];

        // Define o valor formatado no campo
        campo.value = novaData;
    }
}

function formatarDados(event) {
    // Obter o valor do campo de data
    var dataNascimento = document.getElementById("id_data_nascimento").value;

    var regex = /^\d{2}\/\d{2}\/\d{4}$/;
    if (regex.test(dataNascimento)) {
        // Formatar a data de "dd/mm/YYYY" para "YYYY-MM-DD"
        var partesData = dataNascimento.split("/");
        var dia = partesData[0];
        var mes = partesData[1];
        var ano = partesData[2];
        var dataFormatada = ano + "-" + mes + "-" + dia;

        // Atualizar o valor do campo de data com a data formatada
        console.log(dataFormatada)
        document.getElementById("id_data_nascimento").value = dataFormatada;
    }
    // Continuar com o envio do formulário
    event.target.submit();
}

// TRATAMENTO DE CIDADE E ESTADOS

function listarSelects() {
    formatarData2();
    let selectPaises = document.getElementById('id_pais');
    let selectEstados = document.getElementById('id_estado');

    //tempo de execução da requisição da API - definido para 1 minuto

    const timeoutPromise = new Promise((resolve, reject) => {
        setTimeout(() => {
            reject(new Error('Tempo limite excedido'));
        }, 60000);
    });

    //Consumo da API para listar os paises

    Promise.race([
        fetch("https://servicodados.ibge.gov.br/api/v1/localidades/paises?orderBy=nome"),
        timeoutPromise
    ])
        .then(response => {
            if (!response.ok) {
                document.getElementById('errorPopUp').className = "bg-red-400 p-3 rounded-lg text-center";
                document.getElementById('errorPopUpText').innerHTML = "A API de localização demorou muito para responder! <br> Código do status: " + response.status;
            }
            return response.json();
        })
        .then(listaPaises => {
            listaPaises.map(pais => {
                if (pais.nome === "Brasil") {
                    selectPaises.innerHTML += "<option selected value=" + `${pais.nome}` + ">" + `${pais.nome}` + "</option>"
                }
                else {
                    selectPaises.innerHTML += "<option value=" + `${pais.nome}` + ">" + `${pais.nome}` + "</option>"
                }
            })
        })
        .catch(error => {
            document.getElementById('errorPopUp').className = "bg-red-400 p-3 rounded-lg text-center";
            document.getElementById('errorPopUpText').innerHTML = "Ocorreu um erro com a API de localização! <br> Erro:" + error;
        });

    //Consumo da API para listar os estados

    Promise.race([
        fetch("https://servicodados.ibge.gov.br/api/v1/localidades/estados?orderBy=nome"),
        timeoutPromise
    ])
        .then(response => {
            if (!response.ok) {
                document.getElementById('errorPopUp').className = "bg-red-400 p-3 rounded-lg text-center";
                document.getElementById('errorPopUpText').innerHTML = "A API de localização demorou muito para responder! <br> Código do status: " + response.status;
            }
            return response.json();
        })
        .then(listaEstados => {
            listaEstados.map(estado => {
                selectEstados.innerHTML += "<option value=" + `${estado.sigla}` + ">" + `${estado.nome}` + "</option>"

            })
        })
        .catch(error => {
            document.getElementById('errorPopUp').className = "bg-red-400 p-3 rounded-lg text-center";
            document.getElementById('errorPopUpText').innerHTML = "Ocorreu um erro com a API de localização! <br> Erro:" + error;
        });

}

function listarCidades() {
    let SelectCidade = document.getElementById('id_cidade');
    let selectEstados = document.getElementById('id_estado');

    SelectCidade.innerHTML = "<option selected>Selecione a Cidade</option>"

    //tempo de execução da requisição da API - definido para 1 minuto

    const timeoutPromise = new Promise((resolve, reject) => {
        setTimeout(() => {
            reject(new Error('Tempo limite excedido'));
        }, 60000);
    });

    //Consumo da API para listar as cidades

    Promise.race([
        fetch("https://servicodados.ibge.gov.br/api/v1/localidades/estados/" + `${selectEstados.value}` + "/municipios?orderBy=nome"),
        timeoutPromise
    ])
        .then(response => {
            if (!response.ok) {
                document.getElementById('errorPopUp').className = "bg-red-400 p-3 rounded-lg text-center";
                document.getElementById('errorPopUpText').innerHTML = "A API de localização demorou muito para responder! <br> Código do status: " + response.status;
            }
            return response.json();
        })
        .then(listaCidades => {
            listaCidades.map(cidade => {
                SelectCidade.innerHTML += "<option value=" + `${cidade.nome}` + ">" + `${cidade.nome}` + "</option>"

            })
        })
        .catch(error => {
            document.getElementById('errorPopUp').className = "bg-red-400 p-3 rounded-lg text-center";
            document.getElementById('errorPopUpText').innerHTML = "Ocorreu um erro com a API de localização! <br> Erro:" + error;
        });
}

// FORMATAR CELULAR 
function formatarNumeroCelular(id) {
    let numeroCelular = document.getElementById(`${id}`).value;
    numeroCelular = numeroCelular.replace(/\D/g, '');

    let numeroFormatado = '';

    for (let i = 0; i < numeroCelular.length; i++) {
        if (i === 0) {
            numeroFormatado += '(';
        } else if (i === 2) {
            numeroFormatado += ') ';
        } else if (i === 7 && i < 11) {
            numeroFormatado += '-';
        }
        numeroFormatado += numeroCelular[i];
    }

    document.getElementById(`${id}`).value = numeroFormatado;
}

// FORMATADOR DE DATAS
function formatarData(id) {
    let valor = document.getElementById(`${id}`).value;

    valor = valor.replace(/\D/g, "");

    let dataFormatada = '';
    for (let i = 0; i < valor.length; i++) {
        if (i === 2) {
            dataFormatada += '/';
        } else if (i === 4) {
            dataFormatada += '/';
        }
        dataFormatada += valor[i];
    }

    document.getElementById(`${id}`).value = dataFormatada;
}

// TRATAMENTO DA FOTO
function changePhoto() {
    var fileInput = document.getElementById('id_foto_perfil');
    var file = fileInput.files[0];
    var allowedTypes = ['image/jpeg', 'image/png', 'image/jpg'];

    if (!allowedTypes.includes(file.type)) {
        document.getElementById('FotoPacienteError').className = "block mt-1 text-red-500 p-2";
        fileInput.value = '';
        document.getElementById('FotoPacienteError').innerHTML = "Tipo de arquivo não suportado. <br> Por favor, selecione um arquivo JPEG, PNG ou JPG.";
        document.getElementById('IconFotoPaciente').src = "user-icon.png";
    }
    else {
        var image = document.getElementById('IconFotoPaciente');
        image.src = URL.createObjectURL(file);
        document.getElementById('FotoPacienteError').innerHTML = "Enviado com sucesso!";
        document.getElementById('FotoPacienteError').className = "block mt-1 text-green-500 p-2";

    }
}


// VALIDADOR DE EMAIL
function validarEmail(id) {
    let nome = document.getElementById(`${id}`).value;
    let lowercase = nome.toLowerCase();
    document.getElementById(`${id}`).value = lowercase;
}

// MOSTRAR A SENHA
function visibilidadeSenha(idSenha, idIcone) {
    let senhaInput = document.getElementById(`${idSenha}`);
    let icon = document.getElementById(`${idIcone}`);

    if (senhaInput.type === "password") {
        senhaInput.type = "text";
        icon.innerHTML = "<svg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke-width='1.5' stroke='currentColor' class='w-6 h-6'><path stroke-linecap='round' stroke-linejoin='round' d='M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88' /></svg>";
    } else {
        senhaInput.type = "password";
        icon.innerHTML = "<svg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke-width='1.5' stroke='currentColor' class='w-6 h-6'> <path stroke-linecap='round' stroke-linejoin='round' d='M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z' /> <path stroke-linecap='round' stroke-linejoin='round' d='M15 12a3 3 0 11-6 0 3 3 0 016 0z' /></svg>";
    }
}