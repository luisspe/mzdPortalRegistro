# Generated by Django 4.2.4 on 2023-10-02 18:17

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente_Registrado_Portal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.CharField(max_length=100)),
                ('vendedor_id', models.CharField(max_length=100)),
                ('correo', models.CharField(max_length=100)),
                ('nombre', models.CharField(max_length=100)),
                ('numero', models.CharField(max_length=25)),
                ('unidad_de_interes', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='PerfilProspecto',
            fields=[
                ('id_perfil', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('Nombre_Perfil', models.CharField(max_length=255, verbose_name='Nombre del Perfil')),
                ('Rango_Edad', models.CharField(max_length=50, verbose_name='Rango de Edad')),
                ('Tipo_Vehiculo_Interes', models.CharField(choices=[('Económico', 'Económico'), ('De lujo', 'De lujo'), ('Deportivo', 'Deportivo'), ('SUV', 'SUV'), ('Camioneta', 'Camioneta'), ('Otro', 'Otro')], max_length=100, verbose_name='Tipo de Vehículo de Interés')),
                ('Intencion_Compra', models.CharField(choices=[('Inmediata', 'Inmediata'), ('3-6 meses', '3-6 meses'), ('6-12 meses', '6-12 meses'), ('Solo mirando', 'Solo mirando')], max_length=100, verbose_name='Intención de Compra')),
                ('Forma_Pago_Preferida', models.CharField(choices=[('Contado', 'Contado'), ('Crédito', 'Crédito'), ('Leasing', 'Leasing')], max_length=100, verbose_name='Forma de Pago Preferida')),
                ('Ingreso_Mensual', models.CharField(choices=[('< $10,000', '< $10,000'), ('$10,000 - $50,000', '$10,000 - $50,000'), ('> $50,000', '> $50,000')], max_length=100, verbose_name='Ingreso Mensual Aproximado')),
                ('Historial_Credito', models.CharField(choices=[('Excelente', 'Excelente'), ('Bueno', 'Bueno'), ('Regular', 'Regular'), ('Sin historial', 'Sin historial')], max_length=100, verbose_name='Historial de Crédito')),
                ('Potencial_Compra', models.CharField(choices=[('Alto', 'Alto'), ('Medio', 'Medio'), ('Bajo', 'Bajo')], max_length=50, verbose_name='Potencial de Compra o Inversión')),
                ('Vehiculo_Actual', models.CharField(blank=True, max_length=255, null=True, verbose_name='Vehículo Actual (si tiene)')),
                ('datos_adicionales', models.JSONField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Visita',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.CharField(max_length=100)),
                ('vendedor_id', models.CharField(max_length=100)),
                ('unidad_de_interes', models.CharField(max_length=100)),
                ('concepto', models.CharField(max_length=50)),
                ('fecha_hora_checkin', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SpecialEvent',
            fields=[
                ('event_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('prospect_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='mzdportal.perfilprospecto')),
            ],
            options={
                'verbose_name': 'Eventos especiales',
                'verbose_name_plural': 'Eventos especiales',
            },
        ),
        migrations.CreateModel(
            name='Cliente_Registro_Evento',
            fields=[
                ('nombre', models.CharField(max_length=255, verbose_name='Nombre Completo')),
                ('email', models.EmailField(max_length=254, verbose_name='Correo Electrónico')),
                ('telefono', models.CharField(max_length=20, verbose_name='Número de Teléfono')),
                ('client_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('tipo_vehiculo', models.CharField(choices=[('mazda2_sedan', 'MAZDA2 SEDÁN 2024'), ('mazda2_hatchback', 'MAZDA2 HATCHBACK'), ('mazda3_sedan', 'MAZDA3 SEDÁN 2023'), ('mazda3_hatchback', 'MAZDA3 HATCHBACK'), ('mazda_cx3', 'MAZDA CX-3'), ('mazda_cx30', 'MAZDA CX-30'), ('mazda_cx5', 'NUEVA MAZDA CX-5'), ('mazda_cx50', 'MAZDA CX-50'), ('mazda_cx90', 'MAZDA CX-90'), ('mazda_mx5', 'MAZDA MX-5'), ('mazda_mx5_rf', 'MAZDA MX-5 RF')], max_length=50, verbose_name='Tipo de Vehículo')),
                ('como_se_entero', models.CharField(max_length=255, verbose_name='¿Cómo se enteró del evento?')),
                ('recibir_noticias', models.BooleanField(default=False, verbose_name='¿Desea recibir noticias y promociones?')),
                ('metodo_contacto_preferido', models.CharField(choices=[('email', 'Correo Electrónico'), ('telefono', 'Llamada Telefónica'), ('mensaje', 'Mensaje de Texto')], max_length=50, verbose_name='Método de Contacto Preferido')),
                ('interes_financiamiento', models.BooleanField(default=False, verbose_name='¿Está interesado en opciones de financiamiento?')),
                ('vehiculo_parte_pago', models.BooleanField(default=False, verbose_name='¿Tiene un vehículo para dar en parte de pago?')),
                ('valoracion_evento', models.PositiveSmallIntegerField(choices=[(1, '1 - Malo'), (2, '2 - Regular'), (3, '3 - Bueno'), (4, '4 - Muy Bueno'), (5, '5 - Excelente')], verbose_name='Valoración del Evento')),
                ('feedback_evento', models.TextField(blank=True, verbose_name='Sugerencias o Comentarios sobre el Evento')),
                ('evento', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='events', to='mzdportal.specialevent')),
            ],
            options={
                'verbose_name': 'Clientes Registrados en Eventos',
                'verbose_name_plural': 'Clientes Registrados en Eventos',
            },
        ),
    ]
