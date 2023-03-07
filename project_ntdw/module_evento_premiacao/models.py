from django.db import models
import uuid


class Evento(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='Unique ID for this particular entity')
    nome = models.CharField(max_length=200)
    descricao = models.CharField(max_length=200)
    ano = models.IntegerField()
    cronograma_fk = models.ForeignKey('Cronograma', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        """String for representing the Model object."""
        return f'Evento id: {self.id}, nome: {self.nome}, descrição: {self.descricao}, ano do acontecimento: {self.ano}'


class Cronograma(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='Unique ID for this entity')
    data_inicio = models.DateField(null=True, blank=True)
    data_final = models.DateField(null=True, blank=True)
    descricao = models.CharField(max_length=200)

    class Meta:
        ordering = ['id']

    def __str__(self):
        """String for representing the Model object."""
        return f'Cronograma id: {self.id}, descrição: {self.descricao}, data inicial: {self.data_inicio},' \
               f' data final: {self.data_final}'


class Projeto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='Unique ID for this entity')
    titulo = models.CharField(max_length=200)
    resumo = models.CharField(max_length=500)
    data_envio = models.DateField(null=True, blank=True)
    foi_avaliado = models.BooleanField(null=True)
    evento_fk = models.ForeignKey('Evento', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        """String for representing the Model object."""
        return f'Projeto id: {self.id}, titulo: {self.titulo}, resumo: {self.resumo},' \
               f' data de envio: {self.data_envio}, foi avaliado: {self.foi_avaliado}'


class Pessoa(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='Unique ID for this entity')
    nome = models.CharField(max_length=150)
    endereco = models.CharField(max_length=150)
    telefone = models.CharField(max_length=150)
    registro_geral = models.CharField(max_length=20)
    formacao = models.CharField(max_length=100)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'Nome: {self.nome}'


class Autor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='Unique ID for this entity')
    pessoa_id = models.ForeignKey('Pessoa', on_delete=models.SET_NULL, null=True)
    biografia = models.CharField(max_length=500)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.pessoa_id.nome}'


class Join_Projeto_Autor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='Unique ID for this entity')
    projeto_id = models.ForeignKey('Projeto', on_delete=models.SET_NULL, null=True)
    autor_id = models.ForeignKey('Autor', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'Projeto: {self.projeto_id.titulo}, Autor: {self.autor_id.pessoa_id.nome}'


class Avaliador(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='Unique ID for this entity')
    pessoa_id = models.ForeignKey('Pessoa', on_delete=models.SET_NULL, null=True)
    numero_registro_avaliador = models.CharField(max_length=50, null=False)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.pessoa_id.nome}'


class Projeto_Avaliado(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='Unique ID for this entity')
    projeto_id = models.ForeignKey('Projeto', on_delete=models.SET_NULL, null=True)
    avaliador_id = models.ForeignKey('Avaliador', on_delete=models.SET_NULL, null=True)
    parecer = models.CharField(max_length=300, null=False)
    nota = models.DecimalField(max_digits=2, decimal_places=False)
    data_avaliacao = models.DateTimeField(null=False)

    class Meta:
        ordering = ['id']