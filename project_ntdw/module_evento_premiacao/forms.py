from django import forms
from .models import *


class FormCronograma(forms.ModelForm):
    data_inicio = forms.DateField(label='Qual a data de inicio?', widget=forms.SelectDateWidget)
    data_final = forms.DateField(label='Qual a data de termino?', widget=forms.SelectDateWidget)
    descricao = forms.CharField(label='Descrição', widget=forms.Textarea(attrs={"rows": "5", 'placeholder': ''}))

    class Meta:
        model = Cronograma
        fields = ['data_inicio', 'data_final', 'descricao']


class FormEvento(forms.ModelForm):
    nome = forms.CharField(label='Nome do evento:', widget=forms.TextInput(attrs={'placeholder': ''}))
    descricao = forms.CharField(label='Descrição', widget=forms.Textarea(attrs={'rows': '5', 'placeholder': ''}),
                                max_length=200)
    ano = forms.IntegerField(label='Ano do evento:', widget=forms.NumberInput(attrs={'placeholder': ''}))
    cronograma_fk = forms.ModelChoiceField(label='Selecione um cronograma:', queryset=Cronograma.objects.all())

    class Meta:
        model = Evento
        fields = ['nome', 'descricao', 'ano', 'cronograma_fk']


class FormPessoa(forms.ModelForm):
    nome = forms.CharField(label='Nome da pessoa:', widget=forms.TextInput(attrs={'placeholder': ''}))
    endereco = forms.CharField(label='Endereço:', widget=forms.TextInput(attrs={'placeholder': ''}))
    telefone = forms.CharField(label='Telefone:', widget=forms.TextInput(attrs={'placeholder': ''}))
    registro_geral = forms.CharField(label='Nº de registro:', widget=forms.TextInput(attrs={'placeholder': ''}))
    formacao = forms.CharField(label='Formação:', widget=forms.TextInput(attrs={'placeholder': ''}))

    class Meta:
        model = Pessoa
        fields = '__all__'


class FormAutor(forms.ModelForm):
    biografia = forms.CharField(label='Biografia', widget=forms.Textarea(attrs={"rows": "5", 'placeholder': ''}))

    class Meta:
        model = Autor
        fields = ['biografia']


class FormAvaliador(forms.ModelForm):
    numero_registro_avaliador = forms.CharField(label='Nº de registro avaliador:',
                                                widget=forms.Textarea(attrs={"rows": "5", 'placeholder': ''}))

    class Meta:
        model = Avaliador
        fields = ['numero_registro_avaliador']
