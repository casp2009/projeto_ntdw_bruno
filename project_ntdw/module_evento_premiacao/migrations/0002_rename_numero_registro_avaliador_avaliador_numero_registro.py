# Generated by Django 4.1.7 on 2023-05-09 18:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('module_evento_premiacao', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='avaliador',
            old_name='numero_registro_avaliador',
            new_name='numero_registro',
        ),
    ]
