from django.db import models

# Create your models here.
class Visita(models.Model):
    client_id = models.CharField(max_length=100)
    vendedor_id = models.CharField(max_length=100)
    unidad_de_interes = models.CharField(max_length=100)
    estado = models.CharField(max_length=50)
    fecha_hora_checkin = models.DateTimeField(auto_now_add=True)
    fecha_hora_checkout = models.DateTimeField(null=True, blank=True)
    observaciones = models.TextField(blank=True)

    


class SpecialEvent(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    # Otros campos relevantes

    def __str__(self):
        return self.name