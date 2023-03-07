from django.contrib import admin
from module_evento_premiacao.models import *


admin.site.register(Cronograma)
admin.site.register(Evento)
admin.site.register(Projeto)
admin.site.register(Join_Projeto_Autor)
admin.site.register(Autor)
admin.site.register(Pessoa)
admin.site.register(Projeto_Avaliado)
admin.site.register(Avaliador)