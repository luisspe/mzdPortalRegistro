from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Visita  # Importa el modelo de Visita
from django.http import JsonResponse
import requests
from uuid import uuid4


# Configuración de la API
api_url = 'https://5pej009iy2.execute-api.us-east-1.amazonaws.com/dev/apimzd/'
headers = {'x-api-key': 'IUPDlxEc2i2xxCYpmmnGL2JmqhVRkQba1n9Tbl6B'}

# Vista para crear un usuario
def createUser(request):
    return render(request, 'mzdportal/create-account.html')

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
    response = requests.get(f"{api_url}clients/query/{client_info['email']}/", headers=headers)
    if response.status_code == 200:
        client_data = response.json()
        client_id = client_data['client_id']
        num_visits = get_number_of_visits(client_id, headers, api_url)
        event_info["event_data"]["visit"] = f"P{num_visits + 1}"
    else:
        client_id = str(uuid4())
        client_info['client_id'] = client_id
        response = requests.post(f"{api_url}clients/create/", headers=headers, json=client_info)
        if response.status_code == 201:
            event_info["event_data"]['visit'] = "P1"
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
                "visit": 0
            }
        }
        client_id, result = create_event_or_client(request, client_info, event_info, headers, api_url)
        
        # Guardar la visita en la base de datos local
        visita = Visita(
            client_id=client_id,
            vendedor_id=vendedor,
            unidad_de_interes=unidad,
            estado="En Recepción"
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
def perfil_clientes(request):
    context = {}
    return render(request, "mzdportal/clientes.html", context)

# Vista para cerrar sesión
def logout_view(request):
    logout(request)
    return redirect("/")