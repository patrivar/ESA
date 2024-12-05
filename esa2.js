const map = L.map('map').setView([60.23, 24.74], 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
}).addTo(map);

const apiUrl = "http://127.0.0.1:3000/";
const airportMarkers = L.featureGroup().addTo(map);

const blueIcon = L.divIcon({className: "blue-icon"});
const greenIcon = L.divIcon({className: "green-icon"});
/*

 */
async function getStartAirport() {
    try {
        const response = await fetch(apiUrl + "newGame/waltsu");
        if (!response.ok) {
            throw new Error(response.status.toString());
        }
        const airportInfo = await response.json();
        // const startAirport = airportInfo[0].ident;
        console.log(airportInfo);
        markers(airportInfo);
        return airportInfo;

    } catch (error) {
        console.error(error.message);
    }
}
getStartAirport();

function markers(allJson) {
    console.log(allJson);
    const airportInfo = allJson.airports;
    console.log(airportInfo.length);
    for (let i = 0; i < airportInfo.length; i++) {
        console.log(i);
        console.log(airportInfo[i].name, airportInfo[i].latitude_deg, airportInfo[i].longitude_deg);
        if (i === 0) {
            var marker = L.marker([airportInfo[i].latitude_deg, airportInfo[i].longitude_deg]).addTo(map);
            map.flyTo([airportInfo[i].latitude_deg, airportInfo[i].longitude_deg], 10);
            marker.setIcon(greenIcon);
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