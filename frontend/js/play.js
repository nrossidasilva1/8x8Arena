// config
const BOARD_SIZE = 8;
const BROKER_URL = "wss://broker.hivemq.com:8884/mqtt";
const TOPIC_STATE = "8x8arena/state/game";
const TOPIC_CARD = "8x8arena/input/card";
const TOPIC_HAND_PREFIX = "8x8arena/state/hand/";

// colors
const COLOR_GREEN = "#00ff00";
const COLOR_PURPLE = "#a020f0";
const COLOR_FOOD = "#ffff00";
const COLOR_EMPTY = "#1a1a2e";

// dom element
const playerNameEl = document.getElementById("player-name");
const playerTeamEl = document.getElementById("player-team");
const arenaEl = document.getElementById("arena");
const handEl = document.getElementById("hand");
const scoreGreenEl = document.getElementById("score-green");
const scorePurpleEl = document.getElementById("score-purple");


// state
let cells = [];  // arry for cells x , y  (mobile grid) = element div
let mqttClient = null;

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
function buildHand(hand) {
    // create 4 cards
    const placeholder = ["MOVE_UP", "MOVE_DOWN", "MOVE_LEFT", "MOVE_RIGHT"];

    for (let i = 0; i < placeholder.length; i++) {
        const protocolName = placeholder[i];
        const displayName = PROTOCOL_TO_DISPLAY[protocolName];

        const card = document.createElement("div");
        card.className = "card";
        card.textContent = displayName;
        //action when the card is clicked
        card.addEventListener("click", () => playCardProtocol(protocolName));
        handEl.appendChild(card);
    }
    console.log("Player hand built");
}

// render state 
function renderState(state) {
    // clear all cells to empty color
    for (let x = 0; x < BOARD_SIZE; x++) {
        for (let y = 0; y < BOARD_SIZE; y++) {
            cells[x][y].style.backgroundColor = COLOR_EMPTY;
        }
    }
    // green snake in pixels
    for (const pixel of state.snakes.green.pixels) {
        const x = pixel[0];
        const y = pixel[1];
        cells[x][y].style.backgroundColor = COLOR_GREEN;
    }
    // purple snake
    for (const pixel of state.snakes.purple.pixels) {
        const x = pixel[0];
        const y = pixel[1];
        cells[x][y].style.backgroundColor = COLOR_PURPLE;
    }
    // food
    for (const pixel of state.food) {
        const x = pixel[0];
        const y = pixel[1];
        cells[x][y].style.backgroundColor = COLOR_FOOD;
    }
    // update score
    scoreGreenEl.textContent = state.snakes.green.score;
    scorePurpleEl.textContent = state.snakes.purple.score;
}

// setup mqtt
function setupMQTT() {
    mqttClient = mqtt.connect(BROKER_URL);
    mqttClient.on("connect", () => {
        console.log("Connected to broker");
        const nickname = localStorage.getItem("nickname");
        const handTopic = TOPIC_HAND_PREFIX + nickname;
        mqttClient.subscribe(handTopic, (err) => {
            if (err) {
                console.error("Hand subscribe error", err);
            }else {
                console.log("Subscribed to my hand");
            }
        });
        // subscribe the game state
        mqttClient.subscribe(TOPIC_STATE, (err) => {
            if (err) {
                console.error("Subscribe error", err);
            }else {
                console.log("Subscribed to the game state");
            }
        });
    });
    // arrive msg
    mqttClient.on("message", (topic, message) => {
        // parse the msg
        const data = JSON.parse(message.toString());
        // route by topic
        if (topic === TOPIC_STATE) {
            renderState(data);
        }

        // this is my hand?
        const nickname = localStorage.getItem("nickname");
        if (topic === TOPIC_HAND_PREFIX + nickname) {
            renderHand(data.hand);
        }


    });
    mqttClient.on("error", (err) => {
        console.error("MQTT error", err);
    });
}
// protocol - display label
const PROTOCOL_TO_DISPLAY = {
    "MOVE_UP": "UP",
    "MOVE_DOWN": "DOWN",
    "MOVE_LEFT": "LEFT",
    "MOVE_RIGHT": "RIGHT",
    "POWER_PILL": "POWER",
    "TURBO": "TURBO",
};

function renderHand(handCards) {
    // clear the hand
    handEl.innerHTML = "";
    // create card for each real card
    for (let i = 0; i < handCards.length; i++) {
        const protocolName = handCards[i];
        const displayName = PROTOCOL_TO_DISPLAY[protocolName];

        const card = document.createElement("div");
        card.className = "card";
        card.textContent = displayName;
        card.addEventListener("click", () => playCardProtocol(protocolName));
        handEl.appendChild(card);
    }
}
function playCardProtocol(protocolCard) {
    if (mqttClient === null || !mqttClient.connected) {
        console.warn("MQTT not connected");
        return;
    }
    const nickname = localStorage.getItem("nickname");
    const payload = JSON.stringify({
        nickname: nickname,
        card: protocolCard
    });
    mqttClient.publish(TOPIC_CARD, payload, () => {
        console.log(`Played card: ${protocolCard}`);
    });
}




// init
setupHeader();
buildGrid();
buildHand();
setupMQTT();
