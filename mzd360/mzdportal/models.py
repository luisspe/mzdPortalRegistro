from django.db import models
import uuid

class SpecialEvent(models.Model):
    event_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    prospect_profile = models.JSONField(blank=True, null=True)  # Campo para el perfil del prospecto
    # Otros campos relevantes

    def __str__(self):
        return self.name
    

from django.db import models

class PerfilProspecto(models.Model):
    ID_Perfil = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Nombre_Perfil = models.CharField(max_length=255, verbose_name="Nombre del Perfil")
    
    Rango_Edad = models.CharField(max_length=50, verbose_name="Rango de Edad")
    
    Tipo_Vehiculo_Interes = models.CharField(max_length=100, choices=[
        ('Económico', 'Económico'),
        ('De lujo', 'De lujo'),
        ('Deportivo', 'Deportivo'),
        ('SUV', 'SUV'),
        ('Camioneta', 'Camioneta'),
        ('Otro', 'Otro')
    ], verbose_name="Tipo de Vehículo de Interés")
    
    Intencion_Compra = models.CharField(max_length=100, choices=[
        ('Inmediata', 'Inmediata'),
        ('3-6 meses', '3-6 meses'),
        ('6-12 meses', '6-12 meses'),
        ('Solo mirando', 'Solo mirando')
    ], verbose_name="Intención de Compra")
    
    Forma_Pago_Preferida = models.CharField(max_length=100, choices=[
        ('Contado', 'Contado'),
        ('Crédito', 'Crédito'),
        ('Leasing', 'Leasing')
    ], verbose_name="Forma de Pago Preferida")
    
    Ingreso_Mensual = models.CharField(max_length=100, choices=[
        ('< $10,000', '< $10,000'),
        ('$10,000 - $50,000', '$10,000 - $50,000'),
        ('> $50,000', '> $50,000')
    ], verbose_name="Ingreso Mensual Aproximado")
    
    Historial_Credito = models.CharField(max_length=100, choices=[
        ('Excelente', 'Excelente'),
        ('Bueno', 'Bueno'),
        ('Regular', 'Regular'),
        ('Sin historial', 'Sin historial')
    ], verbose_name="Historial de Crédito")
    Potencial_Compra = models.CharField(max_length=50, choices=[
        ('Alto', 'Alto'),
        ('Medio', 'Medio'),
        ('Bajo', 'Bajo')
    ], verbose_name="Potencial de Compra o Inversión")
    
    Vehiculo_Actual = models.CharField(max_length=255, blank=True, null=True, verbose_name="Vehículo Actual (si tiene)")
    
    Observaciones = models.TextField(blank=True, null=True, verbose_name="Observaciones Adicionales")

    def __str__(self):
        return self.Nombre_Perfil


# Create your models here.
class Visita(models.Model):
    client_id = models.CharField(max_length=100)
    vendedor_id = models.CharField(max_length=100)
    unidad_de_interes = models.CharField(max_length=100)
    estado = models.CharField(max_length=50)
    fecha_hora_checkin = models.DateTimeField(auto_now_add=True)
    fecha_hora_checkout = models.DateTimeField(null=True, blank=True)
    


