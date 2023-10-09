from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver

from PIL import Image



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pics/logo_slogan_azul.png', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    # Override the save method of the model
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Make sure to include *args and **kwargs here

        img = Image.open(self.image.path) # Open image

        # resize image
        
        output_size = (200, 200)
        img.thumbnail(output_size) # Resize image
        img.save(self.image.path) # Save it again and override the larger image

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class PerfilProspecto(models.Model):
    id_perfil = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
    
    datos_adicionales = models.JSONField(blank=True, null=True)  # Almacena campos dinámicos

    def __str__(self):
        return self.Nombre_Perfil
    

class SpecialEvent(models.Model):
    event_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    prospect_profile = models.ForeignKey(PerfilProspecto, on_delete=models.CASCADE, related_name="events")
    latitude = models.FloatField(null=True, blank=True)  # Campo para la latitud
    longitude = models.FloatField(null=True, blank=True)  # Campo para la longitud 
    # Otros campos relevantes

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Eventos especiales"
        verbose_name_plural = "Eventos especiales"



class Cliente_Registro_Evento(models.Model):
    nombre = models.CharField(max_length=255, verbose_name="Nombre Completo")
    email = models.EmailField(verbose_name="Correo Electrónico")
    telefono = models.CharField(max_length=20, verbose_name="Número de Teléfono")
    evento = models.ForeignKey(SpecialEvent, on_delete=models.CASCADE, related_name="events", null=True)
    client_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    VEHICULO_INTERES_CHOICES = [
        ('mazda2_sedan', 'MAZDA2 SEDÁN 2024'),
        ('mazda2_hatchback', 'MAZDA2 HATCHBACK'),
        ('mazda3_sedan', 'MAZDA3 SEDÁN 2023'),
        ('mazda3_hatchback', 'MAZDA3 HATCHBACK'),
        ('mazda_cx3', 'MAZDA CX-3'),
        ('mazda_cx30', 'MAZDA CX-30'),
        ('mazda_cx5', 'NUEVA MAZDA CX-5'),
        ('mazda_cx50', 'MAZDA CX-50'),
        ('mazda_cx90', 'MAZDA CX-90'),
        ('mazda_mx5', 'MAZDA MX-5'),
        ('mazda_mx5_rf', 'MAZDA MX-5 RF'),
    ]
    tipo_vehiculo = models.CharField(max_length=50, choices=VEHICULO_INTERES_CHOICES, verbose_name="Tipo de Vehículo")
    
    como_se_entero = models.CharField(max_length=255, verbose_name="¿Cómo se enteró del evento?")
    
    
    recibir_noticias = models.BooleanField(default=False, verbose_name="¿Desea recibir noticias y promociones?")
    METODO_CONTACTO_CHOICES = [
        ('email', 'Correo Electrónico'),
        ('telefono', 'Llamada Telefónica'),
        ('mensaje', 'Mensaje de Texto'),
    ]
    metodo_contacto_preferido = models.CharField(max_length=50, choices=METODO_CONTACTO_CHOICES, verbose_name="Método de Contacto Preferido")
    interes_financiamiento = models.BooleanField(default=False, verbose_name="¿Está interesado en opciones de financiamiento?")
    vehiculo_parte_pago = models.BooleanField(default=False, verbose_name="¿Tiene un vehículo para dar en parte de pago?")
    VALORACION_EVENTO_CHOICES = [
        (1, '1 - Malo'),
        (2, '2 - Regular'),
        (3, '3 - Bueno'),
        (4, '4 - Muy Bueno'),
        (5, '5 - Excelente'),
    ]
    valoracion_evento = models.PositiveSmallIntegerField(choices=VALORACION_EVENTO_CHOICES, verbose_name="Valoración del Evento")
    feedback_evento = models.TextField(verbose_name="Sugerencias o Comentarios sobre el Evento", blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Clientes Registrados en Eventos"
        verbose_name_plural = "Clientes Registrados en Eventos"


# Create your models here.
class Visita(models.Model):
    client_id = models.CharField(max_length=100)
    vendedor_id = models.CharField(max_length=100)
    

    unidad_de_interes = models.CharField(max_length=100)
    concepto = models.CharField(max_length=50)
    fecha_hora_checkin = models.DateTimeField(auto_now_add=True)
    

class Cliente_Registrado_Portal(models.Model):
    client_id = models.CharField(max_length=100)
    vendedor_id = models.CharField(max_length=100)
    correo = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    numero = models.CharField(max_length=25)
    unidad_de_interes = models.CharField(max_length=100)

    


