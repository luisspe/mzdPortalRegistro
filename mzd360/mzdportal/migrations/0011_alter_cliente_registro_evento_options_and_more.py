# Generated by Django 4.2.4 on 2023-09-26 20:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mzdportal', '0010_cliente_registro_evento'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cliente_registro_evento',
            options={'verbose_name': 'Clientes Registrados en Eventos', 'verbose_name_plural': 'Clientes Registrados en Eventos'},
        ),
        migrations.AlterModelOptions(
            name='specialevent',
            options={'verbose_name': 'Eventos especiales', 'verbose_name_plural': 'Eventos especiales'},
        ),
    ]
