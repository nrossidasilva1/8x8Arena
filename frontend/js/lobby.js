// mqtt config
const BROKER_URL = 'wss://broker.hivemq.com:8884/mqtt';
const TOPIC = '8x8arena/players/join';

// dom elements
const nicknameInput = document.getElementById('nickname-input');
const errorMsg = document.getElementById('error-msg');
const greenButton = document.getElementById('join-green');
const purpleButton = document.getElementById('join-purple');

// validatioon nick name 
function validateNickname(nickname) {
    // check range chacters
    if (nickname.length < 2 || nickname.length > 15) {
        return "Nickname must be between 2 and 15 characters , be creative"; // invalid
    }
    // only letters and numbers
    if (!/^[a-zA-Z0-9]+$/.test(nickname)) {
        return "PLease Mate, only letters and numbers is allowed";
    }
    return null; // null = ok  
}

// team join function
function joinTeam(team) {
    // get the wrote value (com.value, and .trim() to remove spaces)
    const nickname = nicknameInput.value.trim();
    // validate 
    const error = validateNickname(nickname);
    if (error !== null) {
        errorMsg.textContent = error;
        return;
    }
    // mistake clean if is validated 
    errorMsg.textContent = "";

    // save in the local storage
    localStorage.setItem('nickname', nickname);
    localStorage.setItem('team', team);

    // mqtt connection
    const client = mqtt.connect(BROKER_URL);

    // if is ok the connection to publish
    client.on('connect', () => {
        console.log("Connected to Broker");
        // set up the payload
        const payload = JSON.stringify({
           nickname: nickname,
           team: team,
           timestamp: Math.floor(Date.now() / 1000) 
        });
        // publish 
        client.publish(TOPIC, payload, () => {
            console.log("Join published");
            window.location.href = 'play.html';
        });

    });

    // conection error
    client.on('error', (err) => {
    console.error("MQTT error:", err);
    errorMsg.textContent = "Sorry we have a connection error!";
    });

}

//  listeners events : button functions
greenButton.addEventListener('click', () => joinTeam('green'));
purpleButton.addEventListener('click', () => joinTeam('purple'));