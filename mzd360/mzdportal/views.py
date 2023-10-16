from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.core.serializers import serialize

from django.urls import reverse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Visita, SpecialEvent, PerfilProspecto, Cliente_Registro_Evento, Cliente_Registrado_Portal
from django.http import JsonResponse
from django.http import HttpResponse
import requests
from uuid import uuid4
from .forms import SpecialEventForm

from datetime import datetime
#credentials
from decouple import config

#excel
import xlwt

# Configuración de la API
api_url = config('API_URL')
API_HEADER_AUTHORIZATION = config('API_KEY')
headers = {
    'x-api-key': API_HEADER_AUTHORIZATION
}





@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile') # Redirect back to profile page

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'mzdportal/profile.html', context)





# Vista para crear un usuario
def createUser(request):
    return render(request, 'mzdportal/create-account.html')

def export_visitas_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Visitas Registradas.xls"'
    
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Visitas Registradas')

    # Define las columnas
    columns = [
        'Nombre', 'Email', 'Teléfono', 'Unidad de Interés',
        'Vendedor', 'Concepto', 'Fecha y Hora de Check-in'
    ]

    # Escribe las columnas en la hoja
    for col_num, column_title in enumerate(columns):
        ws.write(0, col_num, column_title)

    # Obtiene los datos de las visitas
    visitas = Visita.objects.all()

    # Crear una lista para almacenar las tuplas de (visita, cliente)
    visitas_clientes = []

    for visita in visitas:
        
        try:
            cliente = Cliente_Registrado_Portal.objects.get(client_id=visita.client_id)
            visitas_clientes.append((visita, cliente))
        except Cliente_Registrado_Portal.DoesNotExist:
            print(f"El cliente con client_id {visita.client_id} no existe")
            continue

    row_num = 1
    for visita, cliente in visitas_clientes:
        fecha_hora_checkin_str = visita.fecha_hora_checkin.strftime('%Y-%m-%d %H:%M:%S') if isinstance(visita.fecha_hora_checkin, datetime) else visita.fecha_hora_checkin
        row = [
            cliente.nombre, cliente.correo, cliente.numero, visita.unidad_de_interes,
            visita.vendedor_id, visita.concepto, fecha_hora_checkin_str
        ]
        for col_num, cell_value in enumerate(row):
            ws.write(row_num, col_num, cell_value)

        row_num += 1

    wb.save(response)
    return response


def export_clientes_excel(request, event_id):
    response = HttpResponse(content_type='application/ms-excel')
    evento = SpecialEvent.objects.get(event_id=event_id)
    response['Content-Disposition'] = f'attachment; filename="Clientes registrados {evento.name} .xls"'
    
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Clientes Registrados')

    # Define las columnas
    columns = [
        'Nombre', 'Email', 'Teléfono', 'Vehículo de Interés',
        '¿Cómo se enteró?', '¿Desea recibir noticias?', 'Método de Contacto Preferido',
        '¿Interesado en financiamiento?', '¿Vehículo para parte de pago?', 'Valoración del Evento',
        'Feedback del Evento'
    ]

    # Escribe las columnas en la hoja
    for col_num, column_title in enumerate(columns):
        ws.write(0, col_num, column_title)

    # Obtiene los datos de los clientes
    clientes = Cliente_Registro_Evento.objects.all()

    row_num = 1
    for cliente in clientes:
        row = [
            cliente.nombre, cliente.email, cliente.telefono, cliente.get_tipo_vehiculo_display(),
            cliente.como_se_entero, cliente.recibir_noticias, cliente.get_metodo_contacto_preferido_display(),
            cliente.interes_financiamiento, cliente.vehiculo_parte_pago, cliente.get_valoracion_evento_display(),
            cliente.feedback_evento
        ]
        for col_num, cell_value in enumerate(row):
            ws.write(row_num, col_num, cell_value)

        row_num += 1

    wb.save(response)
    return response

# Vista de inicio
@login_required
def home(request):

    return render(request, "mzdportal/home.html", {'user': request.user})

#funcion para buscar cliente con su client_id 
def fetch_client_by_id(request):
    if request.method == 'GET':
        client_id = request.GET.get('client_id', None)
        if client_id:
            response = requests.get(f"{api_url}clients/{client_id}/", headers=headers)
            if response.status_code == 200:
                client_data = response.json()
                return JsonResponse(client_data)
            else:
                return JsonResponse({"error": "Cliente no encontrado"}, status=404)
        else:
            return JsonResponse({"error": "ID del cliente no proporcionado"}, status=400)


# Funcion para buscar client por email y rellenar los campos del formulario automaticamente
def fetch_client_by_email(request):
    if request.method == 'GET':
        email = request.GET.get('email', None)
        if email:
            response = requests.get(f"{api_url}clients/query/{email}/", headers=headers)
            if response.status_code == 200:
                client_data = response.json()
                return JsonResponse(client_data)
            else:
                return JsonResponse({"error": "Cliente no encontrado"}, status=404)
        else:
            return JsonResponse({"error": "Correo electrónico no proporcionado"}, status=400)
        

def fetch_client_visits(request):
    email = request.GET.get('email', None)
    if email:
        # Buscar al cliente por correo electrónico
        client_response = requests.get(f"{api_url}clients/query/{email}/", headers=headers)
        if client_response.status_code == 200:
            client_data = client_response.json()

            # Buscar eventos de tipo "visita" para el cliente
            client_id = client_data['client_id']
            events_response = requests.get(f"{api_url}client/{client_id}/events/", headers=headers)
    
            if events_response.status_code == 200:
                events = events_response.json()
                events_list = events.get('events', [])
                
                visit_events = [event for event in events_list if event['event_type'] == 'visit_registration']
                
                return JsonResponse({'events': visit_events, 'client': client_data})
            else:
                return JsonResponse({'error': 'Eventos de visita no encontrados'}, status=404)

        else:
            return JsonResponse({'error': 'Cliente no encontrado'}, status=404)
    else:
        return JsonResponse({'error': 'Correo electrónico no proporcionado'}, status=400)

# Función para obtener el número de visitas de un cliente
def get_number_of_visits(client_id, headers, api_url):
    response = requests.get(f"{api_url}client/{client_id}/events/", headers=headers)
    if response.status_code == 200:
        events = response.json()
        events_list = events.get('events', [])
        visit_events = [event for event in events_list if event['event_type'] == 'visit']
        num_visits = len(visit_events)
        return num_visits
    else:
        return 0

# Función para crear un evento o un cliente
def create_event_or_client(request, client_info, event_info, headers, api_url):
    """
    Crea un cliente o un evento en la API.
    Si el cliente ya existe, solo crea el evento.
    Si el cliente no existe, primero crea el cliente y luego el evento.
    """
    client_id = None
    response = requests.get(f"{api_url}clients/query/{client_info['email']}/", headers=headers)
    if response.status_code == 200:
        client_data = response.json()
        client_id = client_data['client_id']
        update_response = requests.put(f"{api_url}clients/{client_id}/", headers=headers, json=client_info)
        if update_response.status_code != 200:
            print("Error al actualizar la información del cliente")
            print(update_response.json())  # Esto imprimirá la respuesta completa para que puedas ver qué salió mal

    else:
        if 'client_id' not in client_info:
            client_id = str(uuid4())
            client_info['client_id'] = client_id
        response = requests.post(f"{api_url}clients/create/", headers=headers, json=client_info)
        if response.status_code == 201:
            #event_info["event_data"]['visit'] = "P1"
            if 'client_id' not in event_info:
                event_info['client_id'] = client_id
            response = requests.post(f"{api_url}events/create/", headers=headers, json=event_info)
            return client_id, "Evento creado exitosamente" if response.status_code == 201 else "Error al crear el evento"
    event_info['client_id'] = client_id
    response = requests.post(f"{api_url}events/create/", headers=headers, json=event_info)
    return client_id, "Evento creado exitosamente" if response.status_code == 201 else "Error al crear el evento"

# Vista para manejar visitas
@login_required
def visitas(request):
    context = {}
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        numero = request.POST.get('numero')
        unidad = request.POST.get('unidad')
        vendedor = request.POST.get('vendedor')
        concepto = request.POST.get('concepto')
        client_info = {
            'name': nombre,
            'email': correo,
            'number': numero,
            'unidad_de_interes': unidad,
            'vendedor_asignado': vendedor
        }
        event_info = {
            "event_type": "visit_registration",
            "event_source": "physical_location",
            "event_data": {
                "concept": concepto
            }
        }
        client_id, result = create_event_or_client(request, client_info, event_info, headers, api_url)
        
        # Guardar la visita en la base de datos local
        visita = Visita(
            client_id=client_id,
            vendedor_id=vendedor,
            unidad_de_interes=unidad,
            concepto=concepto
        )

        client_exist = Cliente_Registrado_Portal.objects.filter(client_id=client_id).count()
        if client_exist < 1:

            cliente_registrado_portal = Cliente_Registrado_Portal(
                client_id=client_id,
                vendedor_id=vendedor,
                unidad_de_interes=unidad,
                nombre=nombre,
                correo=correo,
                numero=numero
            )
            cliente_registrado_portal.save()

        visita.save()
        
    # Obtener eventos del día
    events_url = 'https://5pej009iy2.execute-api.us-east-1.amazonaws.com/dev/apimzd/events/today-visits/'
    response = requests.get(events_url, headers=headers)
    events = []
    if response.status_code == 200:
        events_data = response.json()
        for event in events_data:
            client_id = event.get('client_id')
            client_url = f'https://5pej009iy2.execute-api.us-east-1.amazonaws.com/dev/apimzd/clients/{client_id}/'
            client_response = requests.get(client_url, headers=headers)
            if client_response.status_code == 200:
                client_data = client_response.json()
                event['client'] = client_data
                
                events.append(event)
    
    context['page_title'] = 'Control visitas'
    context['events'] = events
    
    return render(request, "mzdportal/visitas.html", context)

# Vista para el perfil de los clientes
@login_required
def perfil_clientes(request):
    context = {}
    return render(request, "mzdportal/clientes.html", context)

@login_required
def eventos(request):
    perfiles_prospecto = PerfilProspecto.objects.all()
    eventos = SpecialEvent.objects.all()
    context = {
        'perfiles_prospecto': perfiles_prospecto,
        'eventos': eventos,
    }
    if request.method == 'POST':
        nombre = request.POST.get('name')
        latitud = request.POST.get('latitud')
        longitud = request.POST.get('longitud')
        fecha_inicio = request.POST.get('start_date')
        fecha_final = request.POST.get('end_date')
        perfil_prospecto_id = request.POST.get('prospect_profile')
        
        # Obtener la instancia de PerfilProspecto usando el ID
        perfil_prospecto_instance = PerfilProspecto.objects.get(Nombre_Perfil=perfil_prospecto_id)
        
        evento = SpecialEvent(
            name=nombre,
            latitude = latitud,
            longitude = longitud,
            start_date=fecha_inicio,
            end_date=fecha_final,
            prospect_profile=perfil_prospecto_instance,  # Asignar la instancia al campo
        )
        evento.save()

    return render(request, "mzdportal/eventos.html", context)

@login_required
def evento_detalle(request, event_id):
    evento = get_object_or_404(SpecialEvent, event_id=event_id)

    return render(request, 'mzdportal/detalles_eventos.html', {'evento': evento})

@login_required
def registro_cliente_evento(request, event_id):
    evento = get_object_or_404(SpecialEvent, event_id=event_id)
    evento_instance = SpecialEvent.objects.get(event_id=evento.event_id)
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        vehiculo_interes = request.POST.get('vehiculo_interes')
        rango_precio = request.POST.get('rango_precio')
        como_se_entero = request.POST.get('entero_evento')
        fecha_compra_estimada = request.POST.get('fecha_compra')
        comentarios = request.POST.get('comentarios')
        recibir_noticias = True if request.POST.get('recibir_noticias') == 'si' else False
        metodo_contacto_preferido = request.POST.get('metodo_contacto')
        interes_financiamiento = True if request.POST.get('interes_financiamiento') == 'si' else False
        vehiculo_parte_pago = True if request.POST.get('vehiculo_parte_pago') == 'si' else False
        valoracion_evento = request.POST.get('valoracion_evento')
        feedback_evento = request.POST.get('feedback_evento')

        cliente = Cliente_Registro_Evento(
            nombre=nombre,
            email=email,
            telefono=telefono,
            tipo_vehiculo=vehiculo_interes,
            como_se_entero=como_se_entero,
            recibir_noticias=recibir_noticias,
            metodo_contacto_preferido=metodo_contacto_preferido,
            interes_financiamiento=interes_financiamiento,
            vehiculo_parte_pago=vehiculo_parte_pago,
            valoracion_evento=valoracion_evento,
            feedback_evento=feedback_evento,
            evento=evento_instance
        )
        cliente.save()



        cliente_instance = Cliente_Registro_Evento.objects.get(email=email)

        client_info = {
            'client_id': str(cliente_instance.client_id),
            'email': email,
            'name': cliente.nombre,
            'number': telefono,
            'unidad_de_interes': vehiculo_interes,
            'vendedor_asignado': "Por asignar",
        }

        event_info = {
            "event_source": "physical_location",
            "event_type": "event_registration",
            "client_id" : str(cliente_instance.client_id),
            "event_data": {
                "concept": evento_instance.name  + " registration",
                "event_id": str(evento_instance.event_id)
            }
        }

        #enviar datos a la api

        client_id, result = create_event_or_client(request, client_info, event_info, headers, api_url)
        if result == "Evento creado exitosamente":
            print("Cliente y evento creados exitosamente")
        else:
            print("Error al crear cliente y evento")
            print(result)  # Esto imprimirá la respuesta completa para que puedas ver qué salió mal

        return redirect(reverse('registro_cliente_evento', args=[evento.event_id]))  # Cambia esto a la URL donde quieres redirigir después de un registro exitoso

    context = {
        'evento': evento,
    }
    return render(request, 'mzdportal/registro_cliente_evento.html', context)

@login_required
def ver_clientes_evento(request, event_id):
    evento = get_object_or_404(SpecialEvent, pk=event_id)
    clientes = Cliente_Registro_Evento.objects.filter(evento=evento)
    return render(request, 'mzdportal/clientesRegistradosEvento.html', {'clientes': clientes, 'evento': evento})

@login_required
def visitas_sucursal_fecha(request):
    context = {}
    if request.method == 'POST':
        fecha_inicio_str = request.POST.get('fecha_inicio')
        fecha_fin_str = request.POST.get('fecha_fin')
        
        fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
        fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
        
        
        visitas = Visita.objects.filter(fecha_hora_checkin__date__range=(fecha_inicio, fecha_fin))

         # Crear una lista para almacenar las tuplas de (visita, cliente)
        visitas_clientes = []

        for visita in visitas:
            try:
                cliente = Cliente_Registrado_Portal.objects.get(client_id=visita.client_id)
                visitas_clientes.append((visita, cliente))
            except Cliente_Registrado_Portal.DoesNotExist:
                print(f"El cliente con client_id {visita.client_id} no existe")

        context['visitas_clientes'] = visitas_clientes
        return render(request, 'mzdportal/visitas_sucursal_por_fecha.html', context)



    return render(request, 'mzdportal/visitas_sucursal_por_fecha.html', context)
# Vista para cerrar sesión
def logout_view(request):
    logout(request)
    return redirect("/")