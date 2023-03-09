from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('cronogramas/', cronogramas, name='cronogramas'),
    path('cronograma_editar/<int:id>', cronograma_editar, name='cronograma_editar'),
    path('cronograma_update/<int:id>', cronograma_update, name='cronograma_update'),
    path('cronograma_delete/<int:id>', cronograma_delete, name='cronograma_delete'),
]