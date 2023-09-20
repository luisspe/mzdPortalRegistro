# Generated by Django 4.2.4 on 2023-09-18 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Visita',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.CharField(max_length=100)),
                ('vendedor_id', models.CharField(max_length=100)),
                ('unidad_de_interes', models.CharField(max_length=100)),
                ('estado', models.CharField(max_length=50)),
                ('fecha_hora_checkin', models.DateTimeField(auto_now_add=True)),
                ('fecha_hora_checkout', models.DateTimeField(blank=True, null=True)),
                ('observaciones', models.TextField(blank=True)),
            ],
        ),
    ]
