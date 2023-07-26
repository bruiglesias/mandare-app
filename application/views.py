from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from . import forms
from . import models
from django.http import Http404
from datetime import date
from itertools import accumulate

# PÁGINAS EXTERNAS DO APP


# LOGIN
def login_page(request):
    form = forms.LoginForm()

    if request.user.is_authenticated:
        return redirect('application:principal')

    return render(request, 'login.html', {
        'form': form,
        'form_action': 'application:autenticar'
    })


def login_redirect_page(request):

    if not request.POST:
        raise Http404()

    form = forms.LoginForm(request.POST)

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('email', ''),
            password=form.cleaned_data.get('password', ''),
        )

        if authenticated_user is not None:
            login(request, authenticated_user)
            return redirect("application:principal")
        else:
            messages.error(request, 'Credenciais inválidas')
    else:
        messages.error(request, 'Usuário ou senha inválidos')

    return render(request, 'login.html', {'form': form})


# CADASTRO
def signup_page(request):
    register_form_data = request.session.get('register_form_data', None)
    form = forms.RegisterForm(register_form_data)

    return render(request, 'cadastro.html', {'form': form})


def signup_redirect(request):

    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST

    form = forms.RegisterForm(POST, request.FILES)

    if form.is_valid():
        form.save()

        messages.success(request, "Usuário cadastrado com sucesso!")
        del (request.session['register_form_data'])
        return redirect("application:index")

    return redirect("application:cadastro")


# PÁGINAS INTERNAS DO APP


# PAGINA INICIAL
@login_required(login_url='application:index')
def main_page(request):

    # Consulta para contar a quantidade de pacientes do usuário
    total_pacientes = models.Paciente.objects.filter(
        profissional=request.user).count()

    # Consulta para contar a quantidade de programas do usuário
    total_programas = models.Programa.objects.filter(
        profissional=request.user).count()

    # Buscas os pacientes do usuário
    pacientes = models.Paciente.objects.filter(
        profissional=request.user
    )

    context = {
        'total_pacientes': total_pacientes,
        'total_programas': total_programas,
        'pacientes': pacientes
    }
    return render(request, 'painel_principal.html', context)


# SAIR
@login_required(login_url='application:index', redirect_field_name='next')
def logout_view(request):
    logout(request)
    return redirect('application:index')


# CADASTRO DE PROGRAMA
@login_required(login_url='application:index')
def add_program_page(request):
    register_form_data = request.session.get('register_form_data', None)
    form = forms.ProgramaForm(register_form_data)
    context = {'form': form}
    return render(request, 'cadastro_programa.html', context)


@login_required(login_url='application:index')
def add_program_redirect(request):

    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST

    form = forms.ProgramaForm(POST)

    if form.is_valid():
        form.save()
        messages.success(request, "Programa cadastrado com sucesso!")
        del (request.session['register_form_data'])

    if not form.is_valid():
        for field, errors in form.errors.items():
            for error in errors:
                # Faça algo com cada mensagem de erro
                print(f"Erro no campo {field}: {error}")

    return redirect("application:cadastrar-programa")


# CADASTRO DE PACIENTE
@login_required(login_url='application:index')
def add_paciente_page(request):
    register_form_data = request.session.get('register_form_data', None)
    form = forms.PacienteForm(register_form_data)
    data_atual = date.today().strftime("%d/%m/%Y")
    context = {
        'form': form,
        'data_atual': data_atual
    }
    return render(request, 'cadastro_paciente.html', context)


@login_required(login_url='application:index')
def add_paciente_redirect(request):

    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST

    form = forms.PacienteForm(POST, request.FILES)

    if form.is_valid():
        form.save()
        messages.success(request, "Paciente cadastrado com sucesso!")
        del (request.session['register_form_data'])

    if not form.is_valid():
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Erro no campo {field}: {error}")

    return redirect("application:cadastrar-paciente")


# BUSCAr PACIENTE
@login_required(login_url='application:index')
def search_main_page(request):

    if request.method == 'POST':

        paciente_id = int(request.POST.get('paciente'))

        # Verificar se o ID do paciente foi fornecido
        if paciente_id > 0:
            try:
                paciente = models.Paciente.objects.get(id=paciente_id)
                return redirect("application:paciente", paciente=paciente.id)

            except models.Paciente.DoesNotExist:
                return redirect("application:principal")

        else:
            # Caso o ID do paciente não tenha sido fornecido
            mensagem = 'Selecione um paciente.'
            messages.error(request, mensagem)
            return redirect("application:principal")

    return redirect("application:principal")


@login_required(login_url='application:index')
def paciente_page(request, paciente):
    try:
        paciente = models.Paciente.objects.get(
            id=paciente, profissional=request.user.id)
    except models.Paciente.DoesNotExist:
        raise Http404()

    programas = models.Programa.objects.filter(
        profissional=request.user)

    context = {
        'paciente': paciente,
        'programas': programas
    }

    return render(request, 'dados_paciente.html', context)


# EDIÇÃO DE PACIENTE
@login_required(login_url='application:index')
def edit_paciente_page(request, id):

    try:
        paciente = models.Paciente.objects.get(
            id=id, profissional=request.user.id)
    except models.Paciente.DoesNotExist:
        raise Http404()

    register_form_data = request.session.get('register_form_data', None)

    form = forms.PacienteForm(register_form_data, instance=paciente)
    data = str(paciente.data_cadastro)
    data = data.split('-')
    nova_data = data[2] + '/' + data[1] + '/' + data[0]
    context = {
        'form': form,
        'paciente': paciente,
        'data_atual': nova_data
    }

    return render(request, 'editar_paciente.html', context)


@login_required(login_url='application:index')
def edit_paciente_redirect(request, id):

    paciente = get_object_or_404(
        models.Paciente, id=id, profissional=request.user.id)

    POST = request.POST
    request.session['register_form_data'] = POST

    form = forms.PacienteForm(POST, request.FILES, instance=paciente)

    if form.is_valid():
        form.save()

        messages.success(request, "Paciente modificado com sucesso!")
        del (request.session['register_form_data'])

    if not form.is_valid():
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Erro no campo {field}: {error}")

    return redirect('application:editar-paciente', id)


# VINCULAR PACIENTE PROGRAMA
@login_required(login_url='application:index')
def add_programa_paciente(request, id):

    if not request.POST:
        raise Http404()

    paciente_id = int(request.POST.get('paciente'))
    programa_id = int(request.POST.get('programa'))

    if programa_id <= 0:
        messages.error(request, "Selecione um programa.")
        return redirect('application:paciente', paciente_id)

    # verificação adicional
    if int(id) != int(paciente_id):
        return redirect('application:paciente', id)

    paciente = get_object_or_404(
        models.Paciente, id=paciente_id, profissional=request.user.id)

    programa = get_object_or_404(
        models.Programa, id=programa_id, profissional=request.user.id)

    programa_paciente, created = models.ProgramaPaciente.objects.get_or_create(
        programa=programa, paciente=paciente)

    return redirect('application:programa-paciente', paciente.id, programa_paciente.id)  # noqa


# VINCULAR PACIENTE PROGRAMA
@login_required(login_url='application:index')
def programa_paciente(request, id_paciente, id_programa):

    programa_paciente = get_object_or_404(
        models.ProgramaPaciente, id=id_programa, programa__profissional=request.user.id)  # noqa

    sessoes = models.Sessao.objects.filter(programa=programa_paciente)

    if request.method == 'POST':

        sessao_valor = int(request.POST.get('SelectSessao'))

        if sessao_valor <= 0:
            context = {
                'id_paciente': id_paciente,
                'programa_paciente': programa_paciente,
                'sessoes': sessoes
            }
            return render(request, 'programa.html', context)

        busca_sessao = get_object_or_404(models.Sessao, id=sessao_valor)
        tentativas = models.Tentativa.objects.filter(sessao=busca_sessao)

        context = {
            'id_paciente': id_paciente,
            'programa_paciente': programa_paciente,
            'sessoes': sessoes,
            'busca_sessao': busca_sessao,
            'tentativas': tentativas
        }

        return render(request, 'programa.html', context)

    context = {
        'id_paciente': id_paciente,
        'programa_paciente': programa_paciente,
        'sessoes': sessoes
    }
    return render(request, 'programa.html', context)


@login_required(login_url='application:index')
def programa_paciente_resumo(request):

    if not request.method == 'POST':
        raise Http404()

    if request.method == 'POST':

        sessao_id = int(request.POST.get('sessao_id'))
        id_paciente = int(request.POST.get('id_paciente'))

        # primeiro salva as atualizações das tentativas
        try:
            programa_paciente_id = int(request.POST.get('programa_paciente'))
            programa_paciente = get_object_or_404(
                    models.ProgramaPaciente, id=programa_paciente_id, programa__profissional=request.user.id)  # noqa

        except:
            programa_paciente_id = int(
                request.POST.get('programa_paciente_id'))
            programa_paciente = get_object_or_404(
                models.ProgramaPaciente, programa__id=programa_paciente_id, programa__profissional=request.user.id)  # noqa

        programa_paciente = get_object_or_404(
            models.ProgramaPaciente, id=programa_paciente_id, programa__profissional=request.user.id)  # noqa

        programa = get_object_or_404(
            models.Programa, id=programa_paciente.programa.id)

        paciente = get_object_or_404(models.Paciente, id=id_paciente)

        # Recuperar a data de nascimento do paciente
        data_nascimento = paciente.data_nascimento

        # Calcular a idade em anos
        data_atual = date.today()
        paciente_idade = data_atual.year - data_nascimento.year

        # Verificar se já fez aniversário este ano ou não
        if data_atual.month < data_nascimento.month:
            paciente_idade -= 1
        elif data_atual.month == data_nascimento.month and data_atual.day < data_nascimento.day:  # noqa
            paciente_idade -= 1

        busca_sessao = get_object_or_404(models.Sessao, id=sessao_id)
        tentativas = models.Tentativa.objects.filter(sessao=busca_sessao)

        data_atual = date.today()
        data_formatada = data_atual.strftime("%d/%m/%Y")

        data = []
        conta_tentativas = 1
        for tentativa in tentativas:

            try:
                tentativa_sim = request.POST.get(
                    f"tentativa_{tentativa.id}_sim")
                tentativa_nao = request.POST.get(
                    f"tentativa_{tentativa.id}_nao")
                tentativa_suporte = request.POST.get(
                    f"tentativa_{tentativa.id}_suporte")

                if tentativa_sim is not None:
                    data.append(
                        {"tentativa_id": tentativa.id, "tentativa_numero": conta_tentativas, "situacao": 'Sim'})  # noqa

                if tentativa_nao is not None:
                    data.append(
                        {"tentativa_id": tentativa.id, "tentativa_numero": conta_tentativas, "situacao": 'Não'})  # noqa

                if tentativa_suporte is not None:
                    data.append(
                        {"tentativa_id": tentativa.id, "tentativa_numero": conta_tentativas, "situacao": 'Suporte'})  # noqa

                conta_tentativas += 1

            except Exception as e:
                continue

        context = {
            "programa_nome": programa.nome,
            "programa_paciente_id": programa_paciente.id,
            "sessao_id": sessao_id,
            "busca_sessao_nome": busca_sessao,
            "id_paciente": id_paciente,
            "paciente_nome": paciente.nome,
            "paciente_idade": paciente_idade,
            "paciente_especialidade": paciente.especialidade,
            "tentativas": data,
            "data_formatada": data_formatada
        }

        return render(request, 'resultado_programa.html', context)

    else:
        raise Http404()


@login_required(login_url='application:index')
def programa_paciente_redirect(request):

    if request.method == 'POST':

        # primeiro salva as atualizações das tentativas

        programa_paciente_id = int(request.POST.get('programa_paciente'))
        sessao_id = int(request.POST.get('sessao_id'))
        id_paciente = int(request.POST.get('id_paciente'))

        programa_paciente = get_object_or_404(
            models.ProgramaPaciente, id=programa_paciente_id, programa__profissional=request.user.id)  # noqa

        paciente = get_object_or_404(models.Paciente, id=id_paciente)

        busca_sessao = get_object_or_404(models.Sessao, id=sessao_id)

        tentativas = models.Tentativa.objects.filter(sessao=busca_sessao)

        for tentativa in tentativas:

            try:
                tentativa_resposta = request.POST.get(
                    f"tentativa_{tentativa.id}")

                if tentativa_resposta == 'Sim':
                    tentativa.situacao = 'Sim'
                    tentativa.save()

                if tentativa_resposta == 'Não':
                    tentativa.situacao = 'Não'
                    tentativa.save()

                if tentativa_resposta == 'Suporte':
                    tentativa.situacao = 'Suporte'
                    tentativa.save()

            except Exception as e:
                print(e.args)
                continue

        messages.success(request, 'Programa atualizado com sucesso!')

        return redirect('application:programa-paciente', id_paciente, programa_paciente.id)  # noqa

    else:
        raise Http404()


@login_required(login_url='application:index')
def historico_page(request, id):
    paciente = get_object_or_404(models.Paciente, id=id)
    programas_do_paciente = models.ProgramaPaciente.objects.filter(
        paciente=paciente)
    context = {'paciente': paciente,
               'programas_do_paciente': programas_do_paciente}
    return render(request, 'historico.html', context)


@login_required(login_url='application:index')
def historico_programa_redirect(request):

    paciente_id = int(request.POST.get('paciente'))
    programa_id = int(request.POST.get('programa'))

    return redirect('application:paciente-programa-historico', paciente_id, programa_id)  # noqa


@login_required(login_url='application:index')
def resultado_historico_page(request, paciente_id, programa_id):

    paciente = get_object_or_404(models.Paciente, id=paciente_id)
    programa_paciente = models.ProgramaPaciente.objects.filter(
        id=programa_id).first()

    sessoes = models.Sessao.objects.filter(programa=programa_paciente)

    dados = []

    for sessao in sessoes:
        tentativas = models.Tentativa.objects.filter(sessao=sessao)
        completa = True
        data = False
        for tentativa in tentativas:

            if tentativa.criado <= tentativa.modificado:
                data_string = tentativa.modificado.strftime('%d/%m/%Y')
                data = data_string

            if tentativa.situacao is None:
                completa = False
                data = False

        if data:
            dados.append(
                {'sessao': sessao, 'complete': completa, 'data': data})
        else:
            dados.append({'sessao': sessao, 'complete': completa})

    context = {
        'paciente_id': paciente_id,
        'programa_id': programa_id,
        'paciente': paciente,
        'programa_paciente': programa_paciente,
        'dados': dados
    }

    return render(request, 'resultado_historico.html', context)


@login_required(login_url='application:index')
def resultado_historico_relatorio(request, paciente_id, programa_id):

    paciente = get_object_or_404(models.Paciente, id=paciente_id)
    programa_paciente = models.ProgramaPaciente.objects.filter(
        id=programa_id).first()

    sessoes = models.Sessao.objects.filter(programa=programa_paciente)

    sessoes_nome = []
    sim = []
    nao = []
    suporte = []

    for sessao in sessoes:
        sessoes_nome.append(sessao.nome)
        tentativas = models.Tentativa.objects.filter(sessao=sessao)
        sessao_sim = 0
        sessao_nao = 0
        sessao_suporte = 0
        sessao_none = 0

        for tentativa in tentativas:
            if tentativa.situacao == 'Sim':
                sessao_sim += 1

            if tentativa.situacao == 'Não':
                sessao_nao += 1

            if tentativa.situacao == 'Suporte':
                sessao_suporte += 1

            if tentativa.situacao is None:
                sessao_none += 1

        if sessao_none == len(tentativas):
            break

        sim.append(sessao_sim)
        nao.append(sessao_nao)
        suporte.append(sessao_suporte)

    """if len(sim) > 0:
        sim = list(accumulate(sim))
    if len(nao) > 0:
        nao = list(accumulate(nao))
    if len(suporte) > 0:
        suporte = list(accumulate(suporte))"""

    context = {
        'paciente_id': paciente_id,
        'programa_id': programa_id,
        'paciente_nome': paciente.nome,
        'programa_nome': programa_paciente.programa.nome,
        'sessoes_nome': sessoes_nome,
        'sim': sim,
        'nao': nao,
        'suporte': suporte

    }
    return render(request, 'relatorio.html', context=context)
