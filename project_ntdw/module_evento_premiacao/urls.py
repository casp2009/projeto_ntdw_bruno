from django.urls import path
from module_evento_premiacao import views

urlpatterns = [
    path('', views.index, name='index'),
]