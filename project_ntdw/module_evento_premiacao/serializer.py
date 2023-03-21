from rest_framework import serializers
from .models import *


class CronogramaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cronograma
        fields = "__all__"


class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = "__all__"


class PessoaSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Pessoa



class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Autor

class AvaliadorSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Avaliador


class ProjetoSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Projeto

class ProjetoAvaliadoSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Projeto_Avaliado