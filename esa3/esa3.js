const map = L.map('map').setView([60.23, 24.74], 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
}).addTo(map);

const apiUrl = "http://127.0.0.1:3000/";
const airportMarkers = L.featureGroup().addTo(map);

const blueIcon = L.divIcon({className: "blue-icon"});
const greenIcon = L.divIcon({className: "green-icon"});
const purpleIcon = L.divIcon({className: "purple-icon"});

async function getStartAirport() {
    try {
        const response = await fetch(apiUrl + "newGame/waltsu");
        if (!response.ok) {
            throw new Error(response.status.toString());
        }
        const airportInfo = await response.json();
        markers(airportInfo);
        return airportInfo;

    } catch (error) {
        console.error(error.message);
    }
}
getStartAirport();

async function markers(allJson) {
    const airportInfo = allJson.airports;
    const gameId = allJson.game_id;
    let currentLocation = allJson.current;

    for (let i = 0; i < airportInfo.length; i++) {
        let marker;
        if (airportInfo[i].ident === currentLocation) {
            marker = L.marker([airportInfo[i].latitude_deg, airportInfo[i].longitude_deg]).addTo(map);
            map.flyTo([airportInfo[i].latitude_deg, airportInfo[i].longitude_deg], 10);
            marker.setIcon(purpleIcon);
        } else {
            marker = L.marker([airportInfo[i].latitude_deg, airportInfo[i].longitude_deg]).addTo(map);
            marker.setIcon(blueIcon);
        }

        const popupContent = document.createElement('div');
        const h4 = document.createElement('h4');
        h4.innerHTML = airportInfo[i].name;
        popupContent.append(h4);
        const goButton = document.createElement('button');
        goButton.classList.add('button');
        goButton.innerHTML = airportInfo[i].ident === currentLocation ? 'Guess here' : 'Fly here';
        popupContent.append(goButton);
        marker.bindPopup(popupContent);

        goButton.addEventListener('click', async function () {
            if (airportInfo[i].ident !== currentLocation) {
                console.log(`Flying to airport: ${airportInfo[i].ident}, Game ID: ${gameId}`);
                await travelToAirport(airportInfo[i].ident, gameId);
                currentLocation = airportInfo[i].ident;
                updateMarkers(allJson, currentLocation);
            }
        });
    }
}

async function travelToAirport(icao, game_id) {
    try {
        const response = await fetch(`${apiUrl}flyto?game=${game_id}&dest=${icao}`);
        if (!response.ok) {
            throw new Error(response.status.toString());
        }
        const data = await response.json();
        console.log('Travel response:', data);
        updateGameState(data);
    } catch (error) {
        console.error('Error traveling to airport:', error);
    }
}

function updateGameState(data) {
    const all_airports = data.all_airports;
    const current_location = data.game_state.location;

    map.eachLayer(function(layer) {
        if (layer instanceof L.Marker) {
            map.removeLayer(layer);
        }
    });

    updateMarkers(data, current_location);

    // Update player information
    document.getElementById('points').textContent = `Pisteet: ${data.game_state.points}`;
    document.getElementById('money').textContent = `Rahat: ${data.game_state.money}`;
    document.getElementById('tries').textContent = `Arvauskerrat: ${data.game_state.tries}`;
}

function updateMarkers(data, currentLocation) {
    const airportInfo = data.all_airports;

    airportInfo.forEach(airport => {
        let marker;
        if (airport.ident === currentLocation) {
            marker = L.marker([airport.latitude_deg, airport.longitude_deg]).addTo(map);
            marker.setIcon(purpleIcon);
        } else {
            marker = L.marker([airport.latitude_deg, airport.longitude_deg]).addTo(map);
            marker.setIcon(blueIcon);
        }

        const popupContent = document.createElement('div');
        const h4 = document.createElement('h4');
        h4.innerHTML = airport.name;
        popupContent.append(h4);
        const goButton = document.createElement('button');
        goButton.classList.add('button');
        goButton.innerHTML = airport.ident === currentLocation ? 'Guess here' : 'Fly here';
        popupContent.append(goButton);
        marker.bindPopup(popupContent);

        goButton.addEventListener('click', async function () {
            if (airport.ident !== currentLocation) {
                console.log(`Flying to airport: ${airport.ident}, Game ID: ${data.game_state.id}`);
                await travelToAirport(airport.ident, data.game_state.id);
            }
        });
    });
}
