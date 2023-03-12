from django.db import models


class Cronograma(models.Model):
    id = models.AutoField(primary_key=True)
    data_inicio = models.DateField(null=True, blank=True)
    data_final = models.DateField(null=True, blank=True)
    descricao = models.CharField(max_length=300, null=True)
    class Meta:
        ordering = ['id']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.descricao}, do dia {self.data_inicio},' \
               f' até o dia {self.data_final}.'


class Evento(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=200)
    descricao = models.CharField(max_length=200)
    ano = models.IntegerField()
    cronograma_fk = models.ForeignKey('Cronograma', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        """String for representing the Model object."""
        return f'Evento id: {self.id}, nome: {self.nome}, descrição: {self.descricao}, ano do acontecimento: {self.ano}'


class Pessoa(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=150)
    endereco = models.CharField(max_length=150)
    telefone = models.CharField(max_length=150)
    registro_geral = models.CharField(max_length=20)
    formacao = models.CharField(max_length=100)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'Id: {self.id}, Nome: {self.nome}'


class Autor(models.Model):
    id = models.AutoField(primary_key=True)
    pessoa = models.OneToOneField(Pessoa, on_delete=models.CASCADE, default=None, null=True)
    biografia = models.CharField(max_length=500)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.pessoa.nome}'


class Projeto(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=200)
    resumo = models.CharField(max_length=500)
    data_envio = models.DateField(null=True, blank=True)
    foi_avaliado = models.BooleanField(null=False, default=False)
    eventos = models.ManyToManyField(Evento)
    autores = models.ManyToManyField(Autor)

    class Meta:
        ordering = ['id']

    def __str__(self):
        """String for representing the Model object."""
        return f'Projeto id: {self.id}, titulo: {self.titulo}, resumo: {self.resumo},' \
               f' data de envio: {self.data_envio}, foi avaliado: {self.foi_avaliado}'


class Avaliador(models.Model):
    id = models.AutoField(primary_key=True)
    pessoa = models.OneToOneField(Pessoa, on_delete=models.CASCADE, default=None, null=True)
    numero_registro_avaliador = models.CharField(max_length=50, null=False)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.pessoa.nome}'


class Projeto_Avaliado(models.Model):
    id = models.AutoField(primary_key=True)
    projeto = models.OneToOneField(Projeto, on_delete=models.CASCADE)
    avaliador = models.OneToOneField(Avaliador, on_delete=models.CASCADE)
    parecer = models.CharField(max_length=300, null=False)
    nota = models.DecimalField(max_digits=2, decimal_places=False)
    data_avaliacao = models.DateTimeField(null=False)

    class Meta:
        ordering = ['id']
