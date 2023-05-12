from datetime import date, datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from .serializer import *
from rest_framework import viewsets
import coreapi

# --------------------- APIs -----------------------

# Cronogramas
class CronogramaViewSetApi(viewsets.ModelViewSet):
    queryset = Cronograma.objects.all()
    serializer_class = CronogramaSerializer
    permission_classes = []


# Evento
class EventoViewSetApi(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    permission_classes = []


# Pessoa
class PessoaViewSetApi(viewsets.ModelViewSet):
    queryset = Pessoa.objects.all()
    serializer_class = PessoaSerializer
    permission_classes = []


# Autor
class AutorViewSetApi(viewsets.ModelViewSet):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer
    permission_classes = []


# Projeto
class ProjetoViewSetApi(viewsets.ModelViewSet):
    queryset = Projeto.objects.all()
    serializer_class = ProjetoSerializer
    permission_classes = []


# Avaliador
class AvaliadorViewSetApi(viewsets.ModelViewSet):
    queryset = Avaliador.objects.all()
    serializer_class = AvaliadorSerializer
    permission_classes = []

#Projeto Avaliado
class ProjetoAvaliadoViewSetApi(viewsets.ModelViewSet):
    queryset = Projeto_Avaliado.objects.all()
    serializer_class = ProjetoAvaliadoSerializer
    permission_classes = []


# --------------------- INDEX --------------------------------
def index(request):
    context = {
        'autor_count': Autor.objects.all().count(),
        'avaliador_count': Avaliador.objects.all().count(),
        'projeto_count': Projeto.objects.all().count(),
        'evento_count': Evento.objects.all().count(),
        'cronograma_count': Cronograma.objects.all().count(),
        'projeto_avaliado_count': Projeto_Avaliado.objects.all().count(),
        'projetos_a_avaliar': Projeto.objects.filter(foi_avaliado=False).count()
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


# -------------------- CRONOGRAMAS --------------------------
def cronogramas(request):
    # Initialize a client & load the schema document
    client = coreapi.Client()
    schema = client.get("http://127.0.0.1:8000/module_evento_premiacao/docs/")

    # Interact with the API endpoint
    action = ["cronogramas", "list"]
    result = client.action(schema, action)
    return render(request, 'cronograma/cronogramas.html', {'cronogramas': result})


def cronograma_delete(request, id):
    client = coreapi.Client()
    schema = client.get("http://127.0.0.1:8000/module_evento_premiacao/docs/")

    # Interact with the API endpoint
    action = ["cronogramas", "delete"]
    params = {
        "id": id,
    }
    client.action(schema, action, params=params)
    return redirect(cronogramas)


def cronograma_editar(request, id):
    cronograma = Cronograma.objects.get(id=id)
    form = FormCronograma(instance=cronograma)

    if request.method == 'GET':
        return render(request, 'cronograma/cronograma_update.html',
                      {'form': form, 'cronograma': cronograma})
    elif request.method == 'POST':
        form = FormCronograma(request.POST, instance=cronograma)
        if form.is_valid():

            cronograma = form.save(commit=False)
            cronograma.descricao = form.cleaned_data['descricao']
            cronograma.data_inicio = form.cleaned_data['data_inicio']
            cronograma.data_final = form.cleaned_data['data_final']
            cronograma.save()

            # Initialize a client & load the schema document
            client = coreapi.Client()
            schema = client.get("http://127.0.0.1:8000/module_evento_premiacao/docs/")

            # Interact with the API endpoint
            action = ["cronogramas", "update"]
            params = {
                "id": id,
                "data_inicio": form.cleaned_data['data_inicio'].isoformat(),
                "data_final": form.cleaned_data['data_final'].isoformat(),
                "descricao": form.cleaned_data['descricao'],
            }
            client.action(schema, action, params=params)

            messages.success(request, 'O cronograma foi alterado com sucesso.')
            return redirect(cronogramas)
        else:
            messages.error(request, 'O formulário é inválido.')
            return render(request, 'cronograma/cronograma_update.html', {'form': form, 'cronograma': cronograma})


def cronograma_create(request):
    form = FormCronograma()
    if request.method == 'POST':
        form = FormCronograma(request.POST)
        if form.is_valid():
            print(form.cleaned_data['data_inicio'])
            # Initialize a client & load the schema document
            client = coreapi.Client()
            schema = client.get("http://127.0.0.1:8000/module_evento_premiacao/docs/")

            # Interact with the API endpoint
            action = ["cronogramas", "create"]
            params = {
                "data_inicio": form.cleaned_data['data_inicio'].isoformat(),
                "data_final": form.cleaned_data['data_final'].isoformat(),
                "descricao": form.cleaned_data['descricao'],
            }
            client.action(schema, action, params=params)
            messages.success(request, 'O cronograma foi criado com sucesso.')
        return redirect(cronogramas)
    elif request.method == 'GET':
        return render(request, 'cronograma/cronograma_create.html', {'form': form})


# -------------------- EVENTOS -----------------

def eventos(request):
    # Initialize a client & load the schema document
    client = coreapi.Client()
    schema = client.get("http://127.0.0.1:8000/module_evento_premiacao/docs/")

    # Interact with the API endpoint
    action1 = ["eventos", "list"]
    action2 = ["cronogramas", "list"]
    result_eventos = client.action(schema, action1)
    result_crono = client.action(schema, action2)
    return render(request, 'evento/eventos.html', {'eventos': result_eventos, 'cronogramas':result_crono})


def evento_delete(request, id):
    client = coreapi.Client()
    schema = client.get("http://127.0.0.1:8000/module_evento_premiacao/docs/")

    # Interact with the API endpoint
    action = ["eventos", "delete"]
    params = {
        "id": id,
    }
    client.action(schema, action, params=params)
    messages.success(request, 'O registro foi deletado.')
    return redirect(eventos)


def evento_editar(request, id):
    evento = Evento.objects.get(id=id)
    form = FormEvento(instance=evento)

    if request.method == 'GET':
        return render(request, 'evento/evento_update.html',
                      {'form': form, 'evento': evento})
    elif request.method == 'POST':
        form = FormEvento(request.POST, instance=evento)
        if form.is_valid():
            client = coreapi.Client()
            schema = client.get("http://127.0.0.1:8000/module_evento_premiacao/docs/")
            # Interact with the API endpoint
            action = ["eventos", "partial_update"]
            params = {
                "id": id,
                "nome": form.cleaned_data['nome'],
                "descricao": form.cleaned_data['descricao'],
                "ano": form.cleaned_data['ano'],
                "cronograma_fk": form.cleaned_data['cronograma_fk'].id,
            }
            client.action(schema, action, params=params)
            messages.success(request, 'O cronograma foi alterado com sucesso.')
            return redirect(eventos)
        else:
            messages.error(request, 'O formulário é inválido.')
            return render(request, 'evento/evento_update.html', {'form': form, 'evento': evento})


def evento_create(request):
    form = FormEvento()
    if request.method == 'POST':
        form = FormEvento(request.POST)
        if form.is_valid():
            client = coreapi.Client()
            schema = client.get("http://127.0.0.1:8000/module_evento_premiacao/docs/")

            # Interact with the API endpoint
            action = ["eventos", "create"]
            params = {
                "nome": form.cleaned_data['nome'],
                "descricao": form.cleaned_data['descricao'],
                "ano": form.cleaned_data['ano'],
                "cronograma_fk": form.cleaned_data['cronograma_fk'].id,
            }
            client.action(schema, action, params=params)
        else:
            messages.error(request, 'O formulário não é válido.')
        return redirect(eventos)
    elif request.method == 'GET':
        return render(request, 'evento/evento_create.html', {'form': form})


# ------------- AUTORES ----------------------

def autores(request):
    # Initialize a client & load the schema document
    client = coreapi.Client()
    schema = client.get("http://127.0.0.1:8000/module_evento_premiacao/docs/")

    # Interact with the API endpoint
    action_autores = ["autores", "list"]
    result_autores = client.action(schema, action_autores)

    action_pessoas = ["pessoas", "list"]
    result_pessoas = client.action(schema, action_pessoas)
    return render(request, 'autor/autores.html', {'autores': result_autores, 'pessoas': result_pessoas})


def autor_create(request):
    form_pessoa = FormPessoa()
    form_autor = FormAutor()
    if request.method == 'POST':
        form_pessoa = FormPessoa(request.POST)
        form_autor = FormAutor(request.POST)

        if form_pessoa.is_valid() and form_autor.is_valid():
            # Initialize a client & load the schema document
            client = coreapi.Client()
            schema = client.get("http://127.0.0.1:8000/module_evento_premiacao/docs/")

            # Interact with the API endpoint
            action = ["pessoas", "create"]
            params = {
                "nome": form_pessoa.cleaned_data['nome'],
                "endereco": form_pessoa.cleaned_data['endereco'],
                "telefone": form_pessoa.cleaned_data['telefone'],
                "registro_geral": form_pessoa.cleaned_data['registro_geral'],
                "formacao": form_pessoa.cleaned_data['formacao'],
            }
            result_pessoa = client.action(schema, action, params=params)

            action = ["autores", "create"]
            params = {
                "biografia": form_autor.cleaned_data['biografia'],
                "pessoa": result_pessoa['id'],
            }
            client.action(schema, action, params=params)
            messages.success(request, 'O autor foi criado com sucesso.')
        else:
            messages.error(request, 'O formulário não é válido.')
        return redirect(autores)
    elif request.method == 'GET':
        return render(request, 'autor/autores_create.html', {'form_pessoa': form_pessoa, 'form_autor': form_autor})


def autores_projetos(request):
    client = coreapi.Client()
    schema = client.get("http://127.0.0.1:8000/module_evento_premiacao/docs/")

    # Interact with autures
    action_autores = ["autores", "list"]
    result_autores = client.action(schema, action_autores)

    # Interact with pessoas
    action_pessoas = ["pessoas", "list"]
    result_pessoas = client.action(schema, action_pessoas)

    # Interact with projetos
    action_projetos = ["projetos", "list"]
    result_projetos = client.action(schema, action_projetos)

    return render(request, 'autor/autores_projetos.html', {'projetos': result_projetos,
                                                           'autores': result_autores, 'pessoas': result_pessoas})


def autor_delete(request, id):
    autor = Autor.objects.get(id=id)
    client = coreapi.Client()
    schema = client.get("http://127.0.0.1:8000/module_evento_premiacao/docs/")

    if autor.pessoa is None:
        pass
    else:
        action_autor = ["autores", "delete"]
        params_autor = {
            "id": id,
        }
        client.action(schema, action_autor, params=params_autor)

        action_pessoa = ["pessoas", "delete"]
        params_pessoa = {
            "id": autor.pessoa.id,
        }
        client.action(schema, action_pessoa, params=params_pessoa)

    messages.success(request, 'O registro foi deletado.')
    return redirect(autores)


def autor_editar(request, id):
    autor = Autor.objects.get(id=id)
    form_autor = FormAutor(instance=autor)

    pessoa = Pessoa.objects.get(id=autor.pessoa.id)
    form_pessoa = FormPessoa(instance=pessoa)

    if request.method == 'GET':
        return render(request, 'autor/autores_update.html',
                      {'form_autor': form_autor, 'form_pessoa': form_pessoa, 'autor': autor})
    elif request.method == 'POST':

        form_autor = FormAutor(request.POST, instance=autor)
        form_pessoa = FormPessoa(request.POST, instance=pessoa)

        if form_autor.is_valid() and form_pessoa.is_valid():
            # Initialize a client & load the schema document
            client = coreapi.Client()
            schema = client.get("http://127.0.0.1:8000/module_evento_premiacao/docs/")

            # Interact with the API endpoint
            action = ["pessoas", "update"]
            params = {
                "id": pessoa.id,
                "nome": form_pessoa.cleaned_data['nome'],
                "endereco": form_pessoa.cleaned_data['endereco'],
                "telefone": form_pessoa.cleaned_data['telefone'],
                "registro_geral": form_pessoa.cleaned_data['registro_geral'],
                "formacao": form_pessoa.cleaned_data['formacao'],
            }
            result_pessoa = client.action(schema, action, params=params)

            action = ["autores", "update"]
            params = {
                "id": id,
                "biografia": form_autor.cleaned_data['biografia'],
                "pessoa": result_pessoa['id'],
            }
            client.action(schema, action, params=params)

            messages.success(request, 'O autor foi alterado com sucesso.')
            return redirect(autores)
        else:
            messages.error(request, 'O formulário é inválido.')
            return render(request, 'autor/autores_update.html', {'form_autor': form_autor, 'form_pessoa': form_pessoa,
                                                                 'autor': autor})


# ------------- AVALIADORES ----------------------

def avaliadores(request):
    client = coreapi.Client()
    schema = client.get("http://127.0.0.1:8000/module_evento_premiacao/docs/")

    # Interact with the API endpoint
    action_avaliadores = ["avaliadores", "list"]
    result_avaliadores = client.action(schema, action_avaliadores)

    action_pessoas = ["pessoas", "list"]
    result_pessoas = client.action(schema, action_pessoas)
    return render(request, 'avaliador/avaliadores.html', {'avaliadores': result_avaliadores, 'pessoas':result_pessoas})


def avaliador_create(request):
    form_pessoa = FormPessoa()
    form_avaliador = FormAvaliador()
    if request.method == 'POST':
        form_pessoa = FormPessoa(request.POST)
        form_avaliador = FormAvaliador(request.POST)

        if form_pessoa.is_valid() and form_avaliador.is_valid():
            client = coreapi.Client()
            schema = client.get("http://127.0.0.1:8000/module_evento_premiacao/docs/")

            # Interact with the API endpoint
            action = ["pessoas", "create"]
            params = {
                "nome": form_pessoa.cleaned_data['nome'],
                "endereco": form_pessoa.cleaned_data['endereco'],
                "telefone": form_pessoa.cleaned_data['telefone'],
                "registro_geral": form_pessoa.cleaned_data['registro_geral'],
                "formacao": form_pessoa.cleaned_data['formacao'],
            }
            result_pessoa = client.action(schema, action, params=params)

            action_avaliador = ["avaliadores", "create"]
            params = {
                "numero_registro": form_avaliador.cleaned_data['numero_registro'],
                "pessoa": result_pessoa['id'],
            }
            client.action(schema, action_avaliador, params=params)
            messages.success(request, 'O avaliador foi criado com sucesso.')
        else:
            messages.error(request, 'O formulário não é válido.')
        return redirect(avaliadores)
    elif request.method == 'GET':
        return render(request, 'avaliador/avaliador_create.html',
                      {'form_pessoa': form_pessoa, 'form_avaliador': form_avaliador})


def avaliador_delete(request, id):
    avaliador = Avaliador.objects.get(id=id)
    client = coreapi.Client()
    schema = client.get("http://127.0.0.1:8000/module_evento_premiacao/docs/")
    if avaliador.pessoa is None:
        action_autor = ["avaliadores", "delete"]
        params_avaliador = {
            "id": id,
        }
        client.action(schema, action_autor, params=params_avaliador)
    else:
        action_avaliador = ["avaliadores", "delete"]
        params_avaliador = {
            "id": id,
        }
        client.action(schema, action_avaliador, params=params_avaliador)

        action_pessoa = ["pessoas", "delete"]
        params_pessoa = {
            "id": avaliador.pessoa.id,
        }
        client.action(schema, action_pessoa, params=params_pessoa)

    messages.success(request, 'O registro foi deletado.')
    return redirect(avaliadores)


def avaliador_editar(request, id):
    avaliador = Avaliador.objects.get(id=id)
    form_avaliador = FormAvaliador(instance=avaliador)

    pessoa = Pessoa.objects.get(id=avaliador.pessoa.id)
    form_pessoa = FormPessoa(instance=pessoa)

    if request.method == 'GET':
        return render(request, 'avaliador/avaliador_update.html',
                      {'form_avaliador': form_avaliador, 'form_pessoa': form_pessoa, 'avaliador': avaliador})
    elif request.method == 'POST':

        form_avaliador = FormAvaliador(request.POST, instance=avaliador)
        form_pessoa = FormPessoa(request.POST, instance=pessoa)

        if form_avaliador.is_valid() and form_pessoa.is_valid():
            client = coreapi.Client()
            schema = client.get("http://127.0.0.1:8000/module_evento_premiacao/docs/")

            # Interact with the API endpoint
            action = ["pessoas", "update"]
            params = {
                "id": pessoa.id,
                "nome": form_pessoa.cleaned_data['nome'],
                "endereco": form_pessoa.cleaned_data['endereco'],
                "telefone": form_pessoa.cleaned_data['telefone'],
                "registro_geral": form_pessoa.cleaned_data['registro_geral'],
                "formacao": form_pessoa.cleaned_data['formacao'],
            }
            result_pessoa = client.action(schema, action, params=params)

            action = ["avaliadores", "update"]
            params = {
                "id": id,
                "numero_registro": form_avaliador.cleaned_data['numero_registro'],
                "pessoa": result_pessoa['id'],
            }
            client.action(schema, action, params=params)

            messages.success(request, 'O avaliador foi alterado com sucesso.')
            return redirect(avaliadores)
        else:
            messages.error(request, 'O formulário é inválido.')
            return render(request, 'avaliador/avaliador_update.html',
                          {'form_avaliador': form_avaliador, 'form_pessoa': form_pessoa,
                           'avaliador': avaliador})


# ------------- PROJETOS ----------------------

def projetos(request):
    # Initialize a client & load the schema document
    client = coreapi.Client()
    schema = client.get("http://127.0.0.1:8000/module_evento_premiacao/docs/")

    # Interact with the API endpoint
    action_projetos = ["projetos", "list"]
    result_projetos = client.action(schema, action_projetos)

    action_autores = ["autores", "list"]
    result_autores = client.action(schema, action_autores)

    action_eventos = ["eventos", "list"]
    result_eventos = client.action(schema, action_eventos)

    action_pessoas = ["pessoas", "list"]
    result_pessoas = client.action(schema, action_pessoas)
    return render(request, 'projetos/projetos.html', {'projetos': result_projetos, 'autores': result_autores, 'eventos': result_eventos,
                                                      'pessoas': result_pessoas})


def projetos_nao_avaliados(request):
    projetos = Projeto.objects.filter(foi_avaliado=False).all()
    return render(request, 'projetos/projetos_nao_avaliados.html', {'projetos': projetos})


def projeto_create(request):
    form = FormProjeto()
    if request.method == 'POST':
        form = FormProjeto(request.POST)
        if form.is_valid():
            # Initialize a client & load the schema document
            client = coreapi.Client()
            schema = client.get("http://127.0.0.1:8000/module_evento_premiacao/docs/")

            # Interact with the API endpoint
            action = ["projetos", "create"]
            autores = []
            eventos = []
            for autor in form.cleaned_data['autores']:
                autores.append(autor.id)
            for evento in form.cleaned_data['eventos']:
                eventos.append(evento.id)
            params = {
                "titulo": form.cleaned_data['titulo'],
                "resumo": form.cleaned_data['resumo'],
                "data_envio": date.today().isoformat(),
                "data_alteracao": date.today().isoformat(),
                "foi_avaliado": False,
                "eventos": eventos,
                "autores": autores,
            }
            client.action(schema, action, params=params)
            messages.success(request, 'O projeto foi criado com sucesso.')
        else:
            messages.error(request, 'O formulário não é válido.')
        return redirect(projetos)
    elif request.method == 'GET':
        return render(request, 'projetos/projeto_create.html', {'form': form})


def projeto_delete(request, id):
    # Initialize a client & load the schema document
    client = coreapi.Client()
    schema = client.get("http://127.0.0.1:8000/module_evento_premiacao/docs/")

    # Interact with the API endpoint
    action = ["projetos", "delete"]
    params = {
        "id": id,
    }
    client.action(schema, action, params=params)
    messages.success(request, 'O projeto foi deletado.')
    return redirect(projetos)


def projeto_editar(request, id):
    projeto = Projeto.objects.get(id=id)
    form = FormProjeto(instance=projeto)

    if request.method == 'GET':
        return render(request, 'projetos/projeto_update.html',
                      {'form': form, 'projeto': projeto})
    elif request.method == 'POST':
        form = FormProjeto(request.POST, instance=projeto)
        if form.is_valid():
            client = coreapi.Client()
            schema = client.get("http://127.0.0.1:8000/module_evento_premiacao/docs/")

            # Interact with the API endpoint
            action = ["projetos", "update"]
            autores = []
            eventos = []
            for autor in form.cleaned_data['autores']:
                autores.append(autor.id)
            for evento in form.cleaned_data['eventos']:
                eventos.append(evento.id)
            params = {
                "id": id,
                "titulo": form.cleaned_data['titulo'],
                "resumo": form.cleaned_data['resumo'],
                "data_envio": projeto.data_envio.isoformat(),
                "data_alteracao": date.today().isoformat(),
                "foi_avaliado": False,
                "eventos": eventos,
                "autores": autores,
            }
            client.action(schema, action, params=params)
            messages.success(request, 'O projeto foi alterado com sucesso.')
            return redirect(projetos)
        else:
            messages.error(request, 'O formulário é inválido.')
            return render(request, 'projeto/projeto_update.html', {'form': form, 'projeto': projeto})


def projeto_avaliar(request, id):
    projeto = Projeto.objects.get(id=id)
    form = FormProjetoAvaliado()
    form.fields['projeto'].initial = projeto
    if request.method == 'POST':
        form = FormProjetoAvaliado(request.POST)
        if form.is_valid():
            # Initialize a client & load the schema document
            client = coreapi.Client()
            schema = client.get("http://127.0.0.1:8000/module_evento_premiacao/docs/")

            # Interact with the API endpoint
            action = ["projeto_avaliado", "create"]
            params = {
                "parecer": form.cleaned_data['parecer'],
                "nota": float(form.cleaned_data['nota']),
                "data_avaliacao": datetime.now().isoformat(),
                "projeto": form.cleaned_data['projeto'].id,
                "avaliador": form.cleaned_data['avaliador'].id,
            }
            client.action(schema, action, params=params)

            action_projeto = ["projetos", "partial_update"]
            params_projeto = {
                "id": id,
                "foi_avaliado": True,
                "data_alteracao": date.today().isoformat(),
            }
            client.action(schema, action_projeto, params=params_projeto)
            messages.success(request, 'O projeto foi avaliado com sucesso.')
        else:
            messages.error(request, 'O formulário não é válido.')
        return redirect(projetos_avaliados)
    elif request.method == 'GET':
        return render(request, 'projetos/projeto_avaliar.html', {'form': form, 'projeto': projeto})


def projetos_avaliados(request):
    return render(request, 'projetos/projetos_avaliados.html', {'avaliacoes': Projeto_Avaliado.objects.all()})


def projetos_rank(request):
    return render(request, 'projetos/projetos_rank.html',
                  {'avaliacoes': Projeto_Avaliado.objects.all().order_by('-nota')})
