const map = L.map('map').setView([60.23, 24.74], 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
}).addTo(map);

const apiUrl = "http://127.0.0.1:3000/";
const airportMarkers = L.featureGroup().addTo(map);

const blueIcon = L.divIcon({className: "blue-icon"});

async function getStartAirport() {
    try {
        const response = await fetch(apiUrl + "getAirports");
        if (!response.ok) {
            throw new Error(response.status.toString());
        }
        const airportInfo = await response.json();
        const startAirport = airportInfo[0].ident;
        return startAirport;

    } catch (error) {
        console.error(error.message);
    }
}
getStartAirport();
/*
const marker = L.marker([airportInfo[0].latitude_deg, airportInfo[0].longitude_deg]);
airportMarkers.addLayer(marker);
marker.setIcon(blueIcon);
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