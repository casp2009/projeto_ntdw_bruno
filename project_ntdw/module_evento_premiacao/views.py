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


def cronograma_update(request, id):
    cronograma = Cronograma.objects.get(id=id)
    cronograma.data_inicio = request.POST.get('data_inicial')
    cronograma.data_final = request.POST.get('data_final')
    cronograma.descricao = request.POST.get('descricao')
    cronograma.save()
    return redirect(cronogramas)

def cronograma_delete(request, id):
    cronograma = Cronograma.objects.get(id=id)
    cronograma.delete()
    return redirect(cronogramas)

def cronograma_editar(request, id):
    return render(request, 'cronograma_update.html', {'cronograma': Cronograma.objects.get(id=id)})
