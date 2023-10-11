document.addEventListener("DOMContentLoaded", function() {
    const searchInput = document.querySelector("input[placeholder='buscar cliente por correo']");
    const mainSearchInput = document.getElementById("mainSearchInput");
    const eventTable = document.querySelector("tbody"); // Asegúrate de que este selector apunte al <tbody> de tu tabla

    function updateTable(events, client) {
        let tableContent = "";

        events.forEach(event => {
            tableContent += `
                <tr class="text-gray-700 dark:text-gray-400">
                    <td class="px-4 py-3">${client.name}</td>
                    <td class="px-4 py-3">${client.email}</td>
                    <td class="px-4 py-3">${client.number}</td>
                    <td class="px-4 py-3">${client.unidad_de_interes}</td>
                    <td class="px-4 py-3">${client.vendedor_asignado}</td>
                    <td class="px-4 py-3">${client.visit}</td>
                    <td class="px-4 py-3">${event.timestamp}</td>
                </tr>
            `;
        });

        eventTable.innerHTML = tableContent;
    }

    function clearTable() {
        eventTable.innerHTML = "";
    }

    function fetchAndUpdate(emailValue) {
        if (emailValue === "") {
            clearTable();
            return;
        }

        if (emailValue.endsWith(".com")) {
            fetch(`/fetch_client_visits/?email=${emailValue}`)
            .then(response => response.json())
            .then(data => {
                if (!data.error) {
                    updateTable(data.events, data.client);
                } else {
                    eventTable.innerHTML = "<tr><td colspan='7'>Cliente no encontrado</td></tr>";
                }
            })
            .catch(error => console.error("Error:", error));
        }
    }

    searchInput.addEventListener("input", function() {
        const emailValue = searchInput.value;
        fetchAndUpdate(emailValue);
    });

    mainSearchInput.addEventListener("input", function() {
        const emailValue = mainSearchInput.value;
        fetchAndUpdate(emailValue);
    });

    



  });