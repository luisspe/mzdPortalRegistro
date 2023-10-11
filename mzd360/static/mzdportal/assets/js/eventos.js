var map;
var geocoder;
var localMarker; // Referencia al marcador de la ubicación local

function initializeMap() {
    geocoder = new google.maps.Geocoder();

    // Inicializar el autocompletado
    var input = document.getElementById('location');
    var autocomplete = new google.maps.places.Autocomplete(input);

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            initMap(position.coords.latitude, position.coords.longitude);
        }, function () {
            alert("Error al obtener la ubicación");
            initMap(); // Coordenadas predeterminadas
        });
    } else {
        alert('Tu navegador no soporta geolocalización');
        initMap(); // Coordenadas predeterminadas
    }
}

function initMap(lat = 20.6736, lng = -103.3440) {
    var userLocation = { lat: lat, lng: lng };

    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 12,
        center: userLocation
    });

    localMarker = new google.maps.Marker({
        position: userLocation,
        map: map,
        draggable: true
    });

    google.maps.event.addListener(localMarker, 'dragend', function () {
        document.getElementById('latitud').value = this.getPosition().lat();
        document.getElementById('longitud').value = this.getPosition().lng();
    });
}

function geocodeAddress() {
    var address = document.getElementById('location').value;
    geocoder.geocode({ 'address': address }, function (results, status) {
        if (status === 'OK') {
            map.setCenter(results[0].geometry.location);
            
            // Elimina el marcador de la ubicación local
            if (localMarker) {
                localMarker.setMap(null);
            }

            // Crea un nuevo marcador en la ubicación buscada
            new google.maps.Marker({
                map: map,
                position: results[0].geometry.location
            });

            document.getElementById('latitud').value = results[0].geometry.location.lat();
            document.getElementById('longitud').value = results[0].geometry.location.lng();
        } else {
            alert('Geocode was not successful: ' + status);
        }
    });
}