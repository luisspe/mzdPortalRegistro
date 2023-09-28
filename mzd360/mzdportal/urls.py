from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic.base import RedirectView


urlpatterns = [
  
    path('',views.visitas),
    path("logout", views.logout_view),
    path("create-account", views.createUser),
    path("visitas", views.visitas, name='visitas-sucursal'),
    path("perfil-clientes", views.perfil_clientes, name='clientes'),
    path('fetch_client/', views.fetch_client_by_email, name='fetch_client_by_email'),
    path('fetch_client_visits/', views.fetch_client_visits, name='fetch_client_visits'),
    path('registro/eventos', views.eventos, name='registro-eventos'),
    path('evento/<uuid:event_id>/', views.evento_detalle, name='evento_detalle'),
    path('registro/cliente/evento/<uuid:event_id>/', views.registro_cliente_evento, name='registro_cliente_evento'),
    path('ver/clientes/evento/<uuid:event_id>/', views.ver_clientes_evento, name='ver_clientes_evento'),
    path('export/excel/<uuid:event_id>', views.export_clientes_excel, name='export_clientes_excel'),
    path('visitas/fecha', views.visitas_sucursal_fecha, name='visitas_fecha'),
    path('export_visitas_excel/', views.export_visitas_excel, name='export_visitas_excel'),
    
]