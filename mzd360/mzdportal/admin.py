from django.contrib import admin
from .models import Visita, SpecialEvent, PerfilProspecto, Cliente_Registro_Evento, Cliente_Registrado_Portal, Profile
# Register your models here.
admin.site.register(Visita)
admin.site.register(SpecialEvent)
admin.site.register(PerfilProspecto)
admin.site.register(Cliente_Registro_Evento)
admin.site.register(Cliente_Registrado_Portal)
admin.site.register(Profile)