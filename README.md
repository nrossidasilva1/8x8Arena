# 8x8Arena 🎮

A crowd-controlled mini-game platform inspired by the classic
"Twitch Plays" experiment. A small grid game runs on the 8×8 LED
matrix of a Raspberry Pi SenseHAT, while remote players send
movement commands from their phones or browsers over MQTT.

## Project Status

🚧 **Work in progress** — Started April 2026 as part of the
*Computer Systems and Networks* module (HDip Computer Science,
2026).

## Architecture (Planned)

Phone and browser clients send commands to an MQTT broker
(Mosquitto running on the Raspberry Pi), which forwards them to a
Python game loop. The game loop processes the inputs and outputs
the result to both the SenseHAT 8×8 LED matrix and a live web
dashboard.

## Tech Stack

- **Hardware:** Raspberry Pi + SenseHAT, Pi Camera Module 3
- **Languages:** Python 3, HTML/CSS/JavaScript
- **Protocols:** MQTT (Mosquitto), HTTP
- **Libraries:** `paho-mqtt`, `sense-hat`, MQTT.js (over WebSockets)
- **Tools:** VS Code, Git & GitHub

## Documentation

- 📄 [Project Proposal](docs/proposal.pdf)

## Author

**Nicolas Rossi da Silva** — Student ID: W20119127  
HDip Computer Science, 2026

## License

MIT License — see [LICENSE](LICENSE) file.
