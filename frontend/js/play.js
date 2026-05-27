// confi
const BOARD_SIZE = 8

// dom element
const playerNameEl = document.getElementById("player-name");
const playerTeamEl = document.getElementById("player-team");
const arenaEl = document.getElementById("arena");
const handEl = document.getElementById("hand");

// state
let cells = [];  // arry for cells x , y  (mobile grid) = element div

// setup header

function setupHeader(){
    // read the local storage with the lobby saved
    const nickname = localStorage.getItem("nickname");
    const team = localStorage.getItem("team");
    // no nick name no team = back to lobby
    if (nickname === null || team === null) {
        console.warn("No nickname or team found, redirecting to lobby");
        window.location.href = "index.html";
        return;
    }

    // fill the header
    playerNameEl.textContent = nickname;
    playerTeamEl.textContent = team.toUpperCase();
}

// grid builder
function buildGrid() {
    // array 2D empty
    for (let x = 0; x < BOARD_SIZE; x++) {
        cells[x] = [];
    }

    // create 64 cells ,nested y inside x
    for (let y = 0; y < BOARD_SIZE; y++) {
        for (let x = 0; x < BOARD_SIZE; x++) {
            // create the div
            const cell = document.createElement("div");
            cell.className = "arena-cell";

            // add the gring into conteiner
            arenaEl.appendChild(cell);

            // save the reference in the array
            cells[x][y] = cell;
        }
    }
    console.log(`Grid build: ${BOARD_SIZE}x${BOARD_SIZE}`);
}

// player hand
function buildHand() {
    // 4 cards 
    const placeholders = ["UP", "RIGHT", "DOWN", "LEFT"];

    for (let i = 0; i < placeholders.length; i++) {
        const card = document.createElement("div");
        card.className = "card";
        card.textContent = placeholders[i];
        
        handEl.appendChild(card);
    }
    console.log("Player hand built");
}

// init
setupHeader();
buildGrid();
buildHand();

