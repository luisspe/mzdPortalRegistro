# Generated by Django 4.2.4 on 2023-09-25 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mzdportal', '0007_remove_perfilprospecto_observaciones_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='specialevent',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='specialevent',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
