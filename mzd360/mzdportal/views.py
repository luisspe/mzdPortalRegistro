from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Visita, SpecialEvent, PerfilProspecto, Cliente_Registro_Evento
from django.http import JsonResponse
from django.http import HttpResponse
import requests
from uuid import uuid4
from .forms import SpecialEventForm

#excel
import xlwt

# Configuración de la API
api_url = 'https://5pej009iy2.execute-api.us-east-1.amazonaws.com/dev/apimzd/'
headers = {'x-api-key': 'IUPDlxEc2i2xxCYpmmnGL2JmqhVRkQba1n9Tbl6B'}

# Vista para crear un usuario
def createUser(request):
    return render(request, 'mzdportal/create-account.html')

def export_clientes_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Clientes registrados.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Clientes')

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
    return render(request, "mzdportal/home.html")

# Vista para buscar un cliente
# @login_required
# def search_client(request, headers, api_url):
#     context = {}
#     if request.method == 'POST':
#         search = request.POST.get('query')
#         print(search)
#         context['search'] = search
#     return render(request, "mzdportal/visitas.html", context)


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
                
                visit_events = [event for event in events_list if event['event_type'] == 'visit']
                
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
    response = requests.get(f"{api_url}clients/query/{client_info['email']}/", headers=headers)
    if response.status_code == 200:
        client_data = response.json()
        client_id = client_data['client_id']
        #num_visits = get_number_of_visits(client_id, headers, api_url)
        #event_info["event_data"]["visit"] = f"P{num_visits + 1}"
    else:
        client_id = str(uuid4())
        client_info['client_id'] = client_id
        response = requests.post(f"{api_url}clients/create/", headers=headers, json=client_info)
        if response.status_code == 201:
            #event_info["event_data"]['visit'] = "P1"
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
            "event_type": "visit",
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

        client_data = {
            'client_id': cliente_instance.client_id,
            'email': email,
            'name': cliente.nombre,
            'number': telefono,
            'unidad_de_interes': vehiculo_interes,
            'vendedor_asignado': "",
        }

        event_data = {
            "event_type": "event registration",
            "client_id" : cliente_instance.client_id,
            "event_data": {
                "concept": evento_instance.name,
                "event_id": evento_instance.event_id
            }
        }

        #enviar datos a la api
        status_code = create_event_or_client(client_data, event_data,headers,api_url)
        if status_code == 200 or status_code ==201:
            print("cliente y evento creeado exitosamente")
        else:
            print("error")
        
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
# Vista para cerrar sesión
def logout_view(request):
    logout(request)
    return redirect("/")