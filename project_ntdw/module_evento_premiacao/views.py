from django.shortcuts import render, redirect
from .models import Autor, Avaliador, Projeto, Evento, Cronograma, Projeto_Avaliado


# Create your views here.
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


def cronogramas(request):
    return render(request, 'cronogramas.html', {'cronogramas': Cronograma.objects.all()})

def cronograma_delete(request, id):
    cronograma = Cronograma.objects.get(id=id)
    cronograma.delete()
    return redirect(cronogramas)

def cronograma_editar(request, id):
    if request.method == 'GET':
        return render(request, 'cronograma_update.html', {'cronograma': Cronograma.objects.get(id=id)})
    elif request.method == 'POST':
        cronograma = Cronograma.objects.get(id=id)
        cronograma.data_inicio = request.POST.get('data_inicial')
        cronograma.data_final = request.POST.get('data_final')
        cronograma.descricao = request.POST.get('descricao')
        cronograma.save()
        return redirect(cronogramas)
def cronograma_create(request):

    if request.method == 'POST':
        dInicial = request.POST.get('data_inicial')
        dFinal = request.POST.get('data_final')
        vdescricao = request.POST.get('descricao')
        Cronograma.objects.create(data_inicio = dInicial, data_final = dFinal, descricao=vdescricao)
        Cronograma.objects.all()
        return redirect(cronogramas)
    elif request.method == 'GET':
        return render(request, 'cronograma_create.html', {})

#-------------EVENTOS----------------#
def eventos(request):
    return render(request, 'eventos.html', {'eventos': Evento.objects.all()})

def evento_delete(request, id):
    evento = Evento.objects.get(id=id)
    evento.delete()
    return redirect(eventos)

def evento_editar(request, id):
    if request.method == 'GET':
        return render(request, 'evento_update.html',
                      {'evento': Evento.objects.get(id=id), 'cronogramas':Cronograma.objects.all()})
    elif request.method == 'POST':
        evento = Evento.objects.get(id=id)
        evento.nome = request.POST.get('nome')
        evento.descricao = request.POST.get('descricao')
        evento.ano = request.POST.get('ano')
        evento.cronograma_fk = Cronograma.objects.get(id=request.POST.get('cronograma_fk'))
        evento.save()
        return redirect(eventos)
def evento_create(request):

    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        ano = request.POST.get('ano')
        cronograma_fk = Cronograma.objects.get(id=request.POST.get('cronograma_fk'))
        Evento.objects.create(nome=nome,descricao=descricao,ano=ano,cronograma_fk=cronograma_fk)
        Evento.objects.all()

        return redirect(eventos)
    elif request.method == 'GET':
        return render(request, 'evento_create.html', {'cronogramas':Cronograma.objects.all()})