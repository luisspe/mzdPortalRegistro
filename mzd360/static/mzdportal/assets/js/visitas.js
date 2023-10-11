document.addEventListener("DOMContentLoaded", function() {
    const emailInput = document.getElementById("correo");
    

    

    emailInput.addEventListener("input", function() {
        const emailValue = emailInput.value;

        if (emailValue.endsWith(".com") || emailValue.endsWith(".mx")) {
            fetch(`/fetch_client/?email=${emailValue}`)
            .then(response => response.json())
            .then(data => {
                if (!data.error) {
                    document.getElementById("nombre").value = data.name || "";
                    document.getElementById("numero").value = data.number || "";
                    document.getElementById("unidad").value = data.unidad_de_interes || "";
                    document.getElementById("vendedor").value = data.vendedor_asignado || "";
                }
            })
            .catch(error => console.error("Error:", error));
        }
    });
});
document.addEventListener("DOMContentLoaded", function() {
    const emailInput = document.getElementById("correo");
    const burger = document.getElementById("burger");

      // Función para ocultar o mostrar el botón burger
    

    emailInput.addEventListener("input", function() {
        const emailValue = emailInput.value;

        // Función para limpiar los campos del formulario
        function clearFields() {
            document.getElementById("nombre").value = "";
            document.getElementById("numero").value = "";
            document.getElementById("unidad").value = "";
            document.getElementById("vendedor").value = "";
        }

        if (emailValue.endsWith(".com")) {
            fetch(`/fetch_client/?email=${emailValue}`)
            .then(response => response.json())
            .then(data => {
                if (!data.error) {
                    document.getElementById("nombre").value = data.name || "";
                    document.getElementById("numero").value = data.number || "";
                    document.getElementById("unidad").value = data.unidad_de_interes || "";
                    document.getElementById("vendedor").value = data.vendedor_asignado || "";
                } else {
                    clearFields();  // Limpia los campos si el cliente no se encuentra
                }
            })
            .catch(error => console.error("Error:", error));
        } else if (emailValue === "") {
            clearFields();  // Limpia los campos si el campo de correo electrónico está vacío
        }
    });
    
});