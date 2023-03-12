from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),

    path('cronogramas/', cronogramas, name='cronogramas'),
    path('cronograma_editar/<int:id>', cronograma_editar, name='cronograma_editar'),
    path('cronograma_delete/<int:id>', cronograma_delete, name='cronograma_delete'),
    path('cronograma_create/', cronograma_create, name='cronograma_create'),

    path('eventos/', eventos, name='eventos'),
    path('evento_editar/<int:id>', evento_editar, name='evento_editar'),
    path('evento_delete/<int:id>', evento_delete, name='evento_delete'),
    path('evento_create/', evento_create, name='evento_create'),

    path('autores/', autores, name='autores'),
    path('autor_editar/<int:id>', autor_editar, name='autor_editar'),
    path('autor_delete/<int:id>', autor_delete, name='autor_delete'),
    path('autor_create/', autor_create, name='autor_create'),

    path('avaliadores/', avaliadores, name='avaliadores'),
    path('avaliador_editar/<int:id>', avaliador_editar, name='avaliador_editar'),
    path('avaliador_delete/<int:id>', avaliador_delete, name='avaliador_delete'),
    path('avaliador_create/', avaliador_create, name='avaliador_create'),

]
