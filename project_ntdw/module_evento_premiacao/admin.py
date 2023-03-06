from django.contrib import admin
from module_evento_premiacao.models import Cronograma, Evento, Projeto

admin.site.register(Cronograma)
admin.site.register(Evento)
admin.site.register(Projeto)
