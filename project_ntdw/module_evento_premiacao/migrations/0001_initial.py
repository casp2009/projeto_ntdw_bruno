# Generated by Django 4.1.7 on 2023-05-09 12:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Autor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('biografia', models.CharField(max_length=500)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Avaliador',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('numero_registro_avaliador', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Cronograma',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('data_inicio', models.DateField(blank=True, null=True)),
                ('data_final', models.DateField(blank=True, null=True)),
                ('descricao', models.CharField(max_length=300, null=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=200)),
                ('descricao', models.CharField(max_length=200)),
                ('ano', models.IntegerField()),
                ('cronograma_fk', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='module_evento_premiacao.cronograma')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Pessoa',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=150)),
                ('endereco', models.CharField(max_length=150)),
                ('telefone', models.CharField(max_length=150)),
                ('registro_geral', models.CharField(max_length=20)),
                ('formacao', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Projeto',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=200)),
                ('resumo', models.CharField(max_length=500)),
                ('data_envio', models.DateField(blank=True, null=True)),
                ('data_alteracao', models.DateField(blank=True, null=True)),
                ('foi_avaliado', models.BooleanField(default=False)),
                ('autores', models.ManyToManyField(to='module_evento_premiacao.autor')),
                ('eventos', models.ManyToManyField(to='module_evento_premiacao.evento')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Projeto_Avaliado',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('parecer', models.CharField(max_length=300)),
                ('nota', models.DecimalField(decimal_places=False, max_digits=2)),
                ('data_avaliacao', models.DateTimeField()),
                ('avaliador', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='module_evento_premiacao.avaliador')),
                ('projeto', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='module_evento_premiacao.projeto')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='avaliador',
            name='pessoa',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='module_evento_premiacao.pessoa'),
        ),
        migrations.AddField(
            model_name='autor',
            name='pessoa',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='module_evento_premiacao.pessoa'),
        ),
    ]