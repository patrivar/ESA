const map = L.map('map').setView([60.23, 24.74], 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
}).addTo(map);

const apiUrl = "http://127.0.0.1:3000/";
const airportMarkers = L.featureGroup().addTo(map);

const blueIcon = L.divIcon({className: "blue-icon"});
const greenIcon = L.divIcon({className: "green-icon"});

async function getStartAirport() {
    try {
        const response = await fetch(apiUrl + "newGame/waltsu");
        if (!response.ok) {
            throw new Error(response.status.toString());
        }
        const airportInfo = await response.json();
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
    const airportGoals = allJson.goals;
    console.log(airportGoals);
    const gameId = allJson.game_id;
    console.log("Game ID:", gameId);
    let currentLocation = allJson.current;
    console.log(currentLocation);

    for (let i = 0; i < airportInfo.length; i++) {
        console.log(i);
        console.log(airportInfo[i].name, airportInfo[i].latitude_deg, airportInfo[i].longitude_deg);

        if (i === 0) {
            var marker = L.marker([airportInfo[i].latitude_deg, airportInfo[i].longitude_deg]).addTo(map);
            map.flyTo([airportInfo[i].latitude_deg, airportInfo[i].longitude_deg], 8);
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
            goButton.addEventListener('click', async function () {
                try {
                    const response = await fetch(`${apiUrl}update?icao=${airportInfo[i].ident}&game_id=${gameId}&points=${allJson.points}&money=${allJson.money}`);
                    if (!response.ok) {
                        throw new Error(response.status.toString());
                    }
                    const data = await response.json();
                    console.log('Update response:', data);
                } catch (error) {
                    console.error('Error updating location:', error);
                }
            });
        } else {
            var marker = L.marker([airportInfo[i].latitude_deg, airportInfo[i].longitude_deg]).addTo(map);
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
            goButton.addEventListener('click', async function () {
                console.log(airportInfo[i]);
                currentLocation = airportInfo[i].ident;
                console.log(currentLocation);
                // goButton.classList.add("hide");
                allJson.money -= 250;
                allJson.points -= 500;
                try {
                    const response = await fetch(`${apiUrl}update?icao=${airportInfo[i].ident}&game_id=${gameId}&points=${allJson.points}&money=${allJson.money}`);
                    if (!response.ok) {
                        throw new Error(response.status.toString());
                    }
                    const data = await response.json();
                    console.log('Update response:', data);
                } catch (error) {
                    console.error('Error updating location:', error);
                }
                map.flyTo([airportInfo[i].latitude_deg, airportInfo[i].longitude_deg], 8);
                for (let g = 0; g < airportGoals.length; g++) {
                    console.log(airportGoals[g]);
                    if (currentLocation === airportGoals[g].airport && airportGoals[g].opened === 0) {
                        setTimeout(async function() {
                            const openChest = "Do you want to open the chest?";
                            if (confirm(openChest) === true) {
                                allJson.money -= 50;
                                airportGoals[g].opened = 1;
                                try {
                                    const response = await fetch(`${apiUrl}updateChest?icao=${airportInfo[i].ident}&game_id=${gameId}&money=${allJson.money}`);
                                    if (!response.ok) {
                                        throw new Error(response.status.toString());
                                    }
                                    const data = await response.json();
                                    console.log('Update chest:', data);
                                } catch (error) {
                                    console.error('Error updating location:', error);
                                }
                            }
                        }, 1200);

                    }
                }
            });
        }
    }
}