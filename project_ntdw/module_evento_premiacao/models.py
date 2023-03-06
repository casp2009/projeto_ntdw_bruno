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