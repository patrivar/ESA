const map = L.map('map').setView([60.23, 24.74], 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
}).addTo(map);

const apiUrl = "http://127.0.0.1:3000/";
const airportMarkers = L.featureGroup().addTo(map);

const blueIcon = L.divIcon({className: "blue-icon"});
const greenIcon = L.divIcon({className: "green-icon"});
const orangeIcon = L.divIcon({className: "orange-icon"});

let playerName = document.querySelector("#name");
let playerPoints = document.querySelector("#points");
let playerMoney = document.querySelector("#money");
let tries = document.querySelector("#tries");
let word = document.querySelector("#word");

const player = prompt("Syötä nimesi: ");
playerName.innerHTML = `Pelaaja: ${player}`;

const winScreen = document.querySelector("#win");
winScreen.classList.add("hide");
const loseScreen = document.querySelector("#lose");
loseScreen.classList.add("hide");

async function getStartAirport() {
    try {
        const response = await fetch(apiUrl + "newGame/" + player);
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
    const letters_found = []
    const goal_letters = allJson.letters;
    console.log(goal_letters);
    const goal_word = allJson.word;
    console.log(goal_word);
    const letter_display = []
    let attempts = 3;


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
            goButton.innerHTML = 'Matkusta ja arvaa sana';
            popupContent.append(goButton);
            marker.bindPopup(popupContent);
            if (allJson.money < 250 || allJson.points === 0) {
                loseScreen.classList.remove("hide");
            } else {
                goButton.addEventListener('click', async function () {
                    allJson.money -= 250;
                    allJson.points -= 500;
                    if (allJson.money < 0) {
                        allJson.money = 0;
                    }
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
                    playerPoints.innerHTML = `Pisteet: ${allJson.points}`;
                    playerMoney.innerHTML = `Rahat: ${allJson.money}`;
                    map.flyTo([airportInfo[i].latitude_deg, airportInfo[i].longitude_deg], 8);
                    setTimeout(async function() {
                        const guess = prompt("Arvaa sana");
                        if (guess === goal_word) {
                            console.log("Arvasit sanan oikein!");
                            winScreen.classList.remove("hide");
                        } else if (attempts >= 1) {
                            attempts -= 1;
                            allJson.points -= 1000;
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
                            alert("Arvasit sanan väärin!");
                            tries.innerHTML = `Arvaukset: ${attempts}`;
                            playerPoints.innerHTML = `Pisteet: ${allJson.points}`;
                            console.log("Arvasit sanan väärin!");
                            console.log("Arvauksia jäljellä: ", attempts);
                        }
                        if (attempts === 0) {
                            console.log("Arvausyrityksesi loppuivat!");
                            loseScreen.classList.remove("hide");
                        }
                    }, 1200);
                });
            }

        } else {
            var marker = L.marker([airportInfo[i].latitude_deg, airportInfo[i].longitude_deg]).addTo(map);
            marker.setIcon(blueIcon);
            const popupContent = document.createElement('div');
            const h4 = document.createElement('h4');
            h4.innerHTML = airportInfo[i].name;
            popupContent.append(h4);
            const goButton = document.createElement('button');
            goButton.classList.add('button');
            goButton.innerHTML = 'Matkusta kohteeseen';
            popupContent.append(goButton);
            marker.bindPopup(popupContent);
            if (allJson.money < 250 || allJson.points === 0) {
                loseScreen.classList.remove("hide");
            } else {
                goButton.addEventListener('click', async function () {
                    console.log(airportInfo[i]);
                    currentLocation = airportInfo[i].ident;
                    console.log(currentLocation);
                    allJson.money -= 250;
                    allJson.points -= 500;
                    if (allJson.money < 0) {
                        allJson.money = 0;
                    }
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
                    playerPoints.innerHTML = `Pisteet: ${allJson.points}`;
                    playerMoney.innerHTML = `Rahat: ${allJson.money}`;
                    map.flyTo([airportInfo[i].latitude_deg, airportInfo[i].longitude_deg], 8);
                    if (allJson.money < 50) {
                        loseScreen.classList.remove("hide");
                    } else {
                        for (let g = 0; g < airportGoals.length; g++) {
                            console.log(airportGoals[g]);
                            if (currentLocation === airportGoals[g].airport && airportGoals[g].opened === 0) {
                                setTimeout(async function() {
                                    const openChest = "Haluatko avata arkun?";
                                    if (confirm(openChest) === true) {
                                        allJson.money -= 50;
                                        if (allJson.money < 0) {
                                            allJson.money = 0;
                                        }
                                        airportGoals[g].opened = 1;
                                        goButton.classList.add("hide");
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
                                        var marker = L.marker([airportInfo[i].latitude_deg, airportInfo[i].longitude_deg]).addTo(map);
                                        marker.setIcon(orangeIcon);
                                        playerMoney.innerHTML = `Rahat: ${allJson.money}`;
                                        if (airportGoals[g].goal === 1) {
                                            allJson.money += 500;
                                            console.log("Löysit 500€!");
                                            alert("Löysit 500€!");
                                        } else if (airportGoals[g].goal === 2) {
                                            allJson.money += 1000;
                                            console.log("Löysit 1000€!");
                                            alert("Löysit 1000€!");
                                        } else if (airportGoals[g].goal === 3) {
                                            console.log("Arkku oli tyhjä.");
                                            alert("Arkku oli tyhjä.");
                                        } else if (airportGoals[g].goal === 4) {
                                            letters_found.push(goal_letters[0]);
                                            goal_letters.shift();
                                            console.log("Löysit kirjaimen", letters_found.slice(-1)[0], "!");
                                            let word_display = "";
                                            for (let j of goal_word) {
                                                if (j === letters_found.slice(-1)[0]) {
                                                    word_display += j;
                                                    letter_display.push(j);
                                                } else if (letter_display.includes(j)) {
                                                    word_display += j;
                                                } else {
                                                    word_display += "_";
                                                }
                                            }
                                            console.log(goal_letters);
                                            console.log(letters_found);
                                            console.log(letter_display);
                                            console.log(word_display);
                                            word.innerHTML = word_display;
                                            alert("Löysit kirjaimen!");
                                        } else {
                                            console.log("Rosvo! Menetit 1000€!");
                                            allJson.money -= 1000;
                                            alert("Rosvo! Menetit 1000€!");
                                        }
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
                                        playerPoints.innerHTML = `Pisteet: ${allJson.points}`;
                                        playerMoney.innerHTML = `Rahat: ${allJson.money}`;
                                    }
                                }, 1200);
                            }
                        }
                    }
                });
            }
        }
    }
}