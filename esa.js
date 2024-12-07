document.addEventListener("DOMContentLoaded", function() {
    const map = L.map('map').setView([51.505, -0.09], 2);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

const apiUrl = "http://127.0.0.1:3000/";
    fetch('http://localhost:5000/get_airports')
        .then(response => response.json())
        .then(data => {
            data.forEach(airport => {
                let circleColor = 'red'; // Default color for out of range
                if (airport.in_range) {
                    circleColor = 'green'; // In range
                }
                if (airport.opened) {
                    circleColor = 'yellow'; // Opened chest
                }
                if (airport.start) {
                    circleColor = 'blue'; // Starting airport
                }
                if (airport.goal) {
                    circleColor = 'purple'; // Airport with a goal
                }

                const circle = L.circle([airport.latitude_deg, airport.longitude_deg], {
                    color: circleColor,
                    fillColor: circleColor,
                    fillOpacity: 0.5,
                    radius: 50000
                }).addTo(map);

                circle.bindPopup(`<b>${airport.name}</b><br>${airport.ident}`);

                circle.on('mouseover', function() {
                    this.openPopup();
                });

                circle.on('mouseout', function() {
                    this.closePopup();
                });

                circle.on('click', function() {
                    if (airport.in_range) {
                        // Travel to the airport
                        travelToAirport(airport.ident);
                    } else {
                        alert("This airport is out of range.");
                    }
                });
            });
        })
        .catch(error => console.error('Error fetching airports:', error));
});

const blueIcon = L.divIcon({className: "blue-icon"});
/*

 */
async function getStartAirport() {
    try {
        const response = await fetch(apiUrl + "getAirports");
        if (!response.ok) {
            throw new Error(response.status.toString());
        }
        const airportInfo = await response.json();
        const startAirport = airportInfo[0].ident;

        // console.log(startAirport);
        markers(airportInfo);
        return startAirport;

    } catch (error) {
        console.error(error.message);
    }
}
getStartAirport();

function markers(airportInfo) {
    console.log(airportInfo);
    console.log(airportInfo.length);
    for (let i = 0; i < airportInfo.length; i++) {
        console.log(i);
        console.log(airportInfo[i].name, airportInfo[i].latitude_deg, airportInfo[i].longitude_deg);
        if (i === 0) {
            var marker = L.marker([airportInfo[i].latitude_deg, airportInfo[i].longitude_deg]).addTo(map);
            map.flyTo([airportInfo[i].latitude_deg, airportInfo[i].longitude_deg], 10);
            marker.setIcon(blueIcon);
            const popupContent = document.createElement('div');
            const h4 = document.createElement('h4');
            h4.innerHTML = airportInfo[i].name;
            popupContent.append(h4);
            const goButton = document.createElement('button');
            goButton.classList.add('button');
            goButton.innerHTML = 'Guess here';
            popupContent.append(goButton);
            marker.bindPopup(popupContent);
            goButton.addEventListener('click', function () {
                /*
            gameSetup(
            `${apiUrl}flyto?game=${gameData.status.id}&dest=${airport.ident}&consumption=${airport.co2_consumption}`
                );
            */
            });
        } else {
            var marker = L.marker([airportInfo[i].latitude_deg, airportInfo[i].longitude_deg]).addTo(map);
            // airportMarkers.addLayer(marker);
            marker.setIcon(blueIcon);
            const popupContent = document.createElement('div');
            const h4 = document.createElement('h4');
            h4.innerHTML = airportInfo[i].name;
            popupContent.append(h4);
            const goButton = document.createElement('button');
            goButton.classList.add('button');
            goButton.innerHTML = 'Fly here';
            popupContent.append(goButton);
            const p = document.createElement('p');
            p.innerHTML = `Distance null km`;
            popupContent.append(p);
            marker.bindPopup(popupContent);
            goButton.addEventListener('click', function () {
            gameSetup(
            `${apiUrl}flyto?game=${gameData.status.id}&dest=${airport.ident}&consumption=${airport.co2_consumption}`
                );
            });
        }


        // when you click on a marker




    }
}
/*

*/
// airportMarkers.clearLayers();

/*
(async () => {
    const startAirport = await getStartAirport();
    if (startAirport) {
        airportMarkers.clearLayers();
        const marker = L.marker([startAirport[0].latitude_deg, startAirport[0].longitude_deg]).addTo(map);
        airportMarkers.addLayer(marker);
        marker.setIcon(blueIcon);
    }
})();
*/


/*
async function gameSetUp(){
    try {

    } catch () {

    }
}

 */