from datetime import date, datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from .forms import *

from .serializer import *
from rest_framework import viewsets, permissions

# --------------------- APIs -----------------------

# Cronogramas
class CronogramaViewSetApi(viewsets.ModelViewSet):
  queryset = Cronograma.objects.all()
  serializer_class = CronogramaSerializer
  permission_classes = [permissions.IsAuthenticated]

# Evento
class EventoViewSetApi(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    permission_classes = [permissions.IsAuthenticated]

# Pessoa
class PessoaViewSetApi(viewsets.ModelViewSet):
    queryset = Pessoa.objects.all()
    serializer_class = PessoaSerializer
    permission_classes = [permissions.IsAuthenticated]

# Autor
class AutorViewSetApi(viewsets.ModelViewSet):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer
    permission_classes = [permissions.IsAuthenticated]

# Projeto
class ProjetoViewSetApi(viewsets.ModelViewSet):
    queryset = Projeto.objects.all()
    serializer_class = ProjetoSerializer
    permission_classes = [permissions.IsAuthenticated]

# Avaliador
class AvaliadorViewSetApi(viewsets.ModelViewSet):
    queryset = Avaliador.objects.all()
    serializer_class = AvaliadorSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProjetoAvaliadoViewSetApi(viewsets.ModelViewSet):
    queryset = Projeto_Avaliado.objects.all()
    serializer_class = ProjetoSerializer
    permission_classes = [permissions.IsAuthenticated]

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
    return render(request, 'cronograma/cronogramas.html', {'cronogramas': Cronograma.objects.all()})


def cronograma_delete(request, id):
    cronograma = Cronograma.objects.get(id=id)
    cronograma.delete()
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
            form.save()
            messages.success(request, 'O cronograma foi criado com sucesso.')
        return redirect(cronogramas)
    elif request.method == 'GET':
        return render(request, 'cronograma/cronograma_create.html', {'form': form})


# -------------------- EVENTOS -----------------

def eventos(request):
    return render(request, 'evento/eventos.html', {'eventos': Evento.objects.all()})


def evento_delete(request, id):
    evento = Evento.objects.get(id=id)
    evento.delete()
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
            evento = form.save(commit=False)
            evento.nome = form.cleaned_data['nome']
            evento.descricao = form.cleaned_data['descricao']
            evento.ano = form.cleaned_data['ano']
            evento.cronograma_fk = form.cleaned_data['cronograma_fk']
            evento.save()
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
            form.save()
            messages.success(request, 'O evento foi criado com sucesso.')
        else:
            messages.error(request, 'O formulário não é válido.')
        return redirect(eventos)
    elif request.method == 'GET':
        return render(request, 'evento/evento_create.html', {'form': form})


# ------------- AUTORES ----------------------

def autores(request):
    return render(request, 'autor/autores.html', {'autores': Autor.objects.all()})


def autor_create(request):
    form_pessoa = FormPessoa()
    form_autor = FormAutor()
    if request.method == 'POST':
        form_pessoa = FormPessoa(request.POST)
        form_autor = FormAutor(request.POST)

        if form_pessoa.is_valid() and form_autor.is_valid():
            pessoa = form_pessoa.save()
            autor = form_autor.save(commit=False)
            autor.pessoa = pessoa
            autor.save()
            messages.success(request, 'O autor foi criado com sucesso.')
        else:
            messages.error(request, 'O formulário não é válido.')
        return redirect(autores)
    elif request.method == 'GET':
        return render(request, 'autor/autores_create.html', {'form_pessoa': form_pessoa, 'form_autor': form_autor})


def autores_projetos(request):
    autores = Autor.objects.all()
    projetos = Projeto.objects.all()
    autoresFinal = []
    for autor in autores:
        for projeto in projetos:
            for at2 in projeto.autores.all():
                if autor.pessoa.nome == at2.pessoa.nome:
                    autoresFinal.append(autor)
    lista_sem_duplicados = list(set(autoresFinal))
    return render(request, 'autor/autores_projetos.html', {'projetos': Projeto.objects.all(),
                                                           'autores': lista_sem_duplicados})


def autor_delete(request, id):
    autor = Autor.objects.get(id=id)
    if autor.pessoa is None:
        pass
    else:
        pessoa = Pessoa.objects.get(id=autor.pessoa.id)
        pessoa.delete()
    messages.success(request, 'O registro foi deletado.')
    autor.delete()
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
            pessoa = form_pessoa.save(commit=False)
            pessoa.nome = form_pessoa.cleaned_data['nome']
            pessoa.endereco = form_pessoa.cleaned_data['endereco']
            pessoa.telefone = form_pessoa.cleaned_data['telefone']
            pessoa.registro_geral = form_pessoa.cleaned_data['registro_geral']
            pessoa.formacao = form_pessoa.cleaned_data['formacao']
            pessoa.save()

            autor = form_autor.save(commit=False)
            autor.biografia = form_autor.cleaned_data['biografia']
            autor.save()

            messages.success(request, 'O autor foi alterado com sucesso.')
            return redirect(autores)
        else:
            messages.error(request, 'O formulário é inválido.')
            return render(request, 'autor/autores_update.html', {'form_autor': form_autor, 'form_pessoa': form_pessoa,
                                                                 'autor': autor})


# ------------- AVALIADORES ----------------------

def avaliadores(request):
    return render(request, 'avaliador/avaliadores.html', {'avaliadores': Avaliador.objects.all()})


def avaliador_create(request):
    form_pessoa = FormPessoa()
    form_avaliador = FormAvaliador()
    if request.method == 'POST':
        form_pessoa = FormPessoa(request.POST)
        form_avaliador = FormAvaliador(request.POST)

        if form_pessoa.is_valid() and form_avaliador.is_valid():
            pessoa = form_pessoa.save()
            avaliador = form_avaliador.save(commit=False)
            avaliador.pessoa = pessoa
            avaliador.save()
            messages.success(request, 'O avaliador foi criado com sucesso.')
        else:
            messages.error(request, 'O formulário não é válido.')
        return redirect(autores)
    elif request.method == 'GET':
        return render(request, 'avaliador/avaliador_create.html',
                      {'form_pessoa': form_pessoa, 'form_avaliador': form_avaliador})


def avaliador_delete(request, id):
    avaliador = Avaliador.objects.get(id=id)
    if avaliador.pessoa is None:
        pass
    else:
        pessoa = Pessoa.objects.get(id=avaliador.pessoa.id)
        pessoa.delete()

    messages.success(request, 'O registro foi deletado.')
    avaliador.delete()
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
            pessoa = form_pessoa.save(commit=False)
            pessoa.nome = form_pessoa.cleaned_data['nome']
            pessoa.endereco = form_pessoa.cleaned_data['endereco']
            pessoa.telefone = form_pessoa.cleaned_data['telefone']
            pessoa.registro_geral = form_pessoa.cleaned_data['registro_geral']
            pessoa.formacao = form_pessoa.cleaned_data['formacao']
            pessoa.save()

            avaliador = form_avaliador.save(commit=False)
            avaliador.numero_registro_avaliador = form_avaliador.cleaned_data['numero_registro_avaliador']
            avaliador.save()

            messages.success(request, 'O avaliador foi alterado com sucesso.')
            return redirect(avaliadores)
        else:
            messages.error(request, 'O formulário é inválido.')
            return render(request, 'avaliador/avaliador_update.html',
                          {'form_avaliador': form_avaliador, 'form_pessoa': form_pessoa,
                           'avaliador': avaliador})


# ------------- PROJETOS ----------------------

def projetos(request):
    return render(request, 'projetos/projetos.html', {'projetos': Projeto.objects.all()})


def projetos_nao_avaliados(request):
    projetos = Projeto.objects.filter(foi_avaliado=False).all()
    return render(request, 'projetos/projetos_nao_avaliados.html', {'projetos': projetos})


def projeto_create(request):
    form = FormProjeto()
    if request.method == 'POST':
        form = FormProjeto(request.POST)
        if form.is_valid():
            projeto = form.save(commit=False)
            projeto.foi_avaliado = False
            projeto.data_envio = date.today()
            projeto.data_alteracao = date.today()
            projeto.save()
            projeto.autores.set(form.cleaned_data['autores'])
            projeto.eventos.set(form.cleaned_data['eventos'])
            messages.success(request, 'O projeto foi criado com sucesso.')
        else:
            messages.error(request, 'O formulário não é válido.')
        return redirect(projetos)
    elif request.method == 'GET':
        return render(request, 'projetos/projeto_create.html', {'form': form})


def projeto_delete(request, id):
    projeto = Projeto.objects.get(id=id)
    projeto.delete()
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
            projeto = form.save(commit=False)
            projeto.titulo = form.cleaned_data['titulo']
            projeto.resumo = form.cleaned_data['resumo']
            projeto.data_alteracao = date.today()
            projeto.autores.set(form.cleaned_data['autores'])
            projeto.eventos.set(form.cleaned_data['eventos'])
            projeto.save()
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
            projeto_avaliado = form.save(commit=False)
            projeto_avaliado.avaliador = form.cleaned_data['avaliador']
            projeto_avaliado.data_avaliacao = datetime.now()
            projeto_escolhido = form.cleaned_data['projeto']
            projeto_escolhido.foi_avaliado = True
            projeto_escolhido.save()
            projeto_avaliado.save()
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
