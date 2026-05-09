# 8x8Arena — How the Devices Talk to Each Other

**Version:** 1.0 (first draft, will probably change as I build it)
**Last updated:** May 2026
**Broker:** HiveMQ public broker — `broker.hivemq.com`

> This is my notes about how messages flow between the players and
> the Raspberry Pi. Things may change once I start coding and find
> stuff that doesn't work the way I imagined.

---

## The big picture

The whole game is basically a bunch of small messages flying around.
Players send "I just played this card" and the Pi sends back "ok,
here is the new state of the snakes". Everything goes through a
broker (HiveMQ) so I don't have to worry about each device knowing
the address of every other device.

```
   Phones / Browsers  ── plays a card ──►  HiveMQ broker  ──►  Raspberry Pi
                                                                     │
                                                              tick happens
                                                                     │
   Phones / Browsers  ◄─── sends state ───  HiveMQ broker  ◄────────┘
```

The match starts when someone presses the **SenseHAT joystick** on
the Pi (the button on the board). Until then the Pi just shows a
"waiting" screen on the LED matrix.

---

## Two ways to play

The game supports two modes at the same time — both work with the
same code, the difference is just where the players are.

**Local console mode**
Everyone is in the same room, watching the SenseHAT directly. Their
phones connect over WiFi to send commands. Feels like an old arcade
machine.

**Remote mode**
Players are anywhere in the world. The Raspberry Pi Camera Module 3
streams a live video of the LED matrix to a webpage so remote players
can see what is happening on the board.

Both modes use the exact same MQTT topics. The camera stream is just
an extra video feed running in parallel — it does not change anything
about the game logic.

---

## The topics (channels of communication)

I split the topics in two groups: things players send to the Pi,
and things the Pi sends back.

### Players talking to the Pi

| Topic                         | What it means                          |
|-------------------------------|----------------------------------------|
| `8x8arena/players/join`       | A new player entered the arena         |
| `8x8arena/players/leave`      | A player left or closed the browser    |
| `8x8arena/input/card`         | A player tapped a card on their phone  |

### The Pi talking back to players

| Topic                              | What it carries                          |
|------------------------------------|------------------------------------------|
| `8x8arena/state/game`              | The full game state, sent every tick     |
| `8x8arena/state/hand/{nickname}`   | The 4 cards in a specific player's hand  |
| `8x8arena/state/players`           | Who is connected and on which team       |
| `8x8arena/state/winner`            | Match result when someone wins           |
| `8x8arena/leaderboard`             | Updated top scores                       |

The reason the hand topic has the nickname inside is that each
player should only see their own cards, not the other players'.
So `8x8arena/state/hand/joao` is private to João.

---

## What the messages look like

All messages are JSON. I picked JSON because it's the easiest format
to read both in Python (Pi side) and JavaScript (browser side).
Everything is sent as a UTF-8 string.

### When a player joins

```json
{
  "nickname": "joao",
  "timestamp": 1717000000
}
```

### When a player leaves

Same format, just on a different topic.

```json
{
  "nickname": "joao",
  "timestamp": 1717000000
}
```

### When a player plays a card

```json
{
  "nickname": "joao",
  "card": "MOVE_UP",
  "timestamp": 1717000000
}
```

The card field can be one of: `MOVE_UP`, `MOVE_DOWN`, `MOVE_LEFT`,
`MOVE_RIGHT`, `POWER_PILL`, `TURBO`.

### The game state (sent every tick)

This is the big one. It carries everything that's happening on the
board: where each snake is, the score, whether power pill or turbo
are active, and where the food is.

```json
{
  "tick": 42,
  "snakes": {
    "green": {
      "pixels": [[2,3], [2,4], [2,5]],
      "score": 4,
      "powerPillActive": false,
      "turboActive": false
    },
    "purple": {
      "pixels": [[5,5], [5,6]],
      "score": 2,
      "powerPillActive": false,
      "turboActive": true
    }
  },
  "food": [[1,1], [6,3]],
  "status": "playing"
}
```

Status can be `waiting` (before someone presses the joystick),
`playing`, or `finished`. Pixel positions are `[column, row]` on
the 8x8 grid.

### The hand of one player

```json
{
  "nickname": "joao",
  "team": "green",
  "cards": ["MOVE_UP", "MOVE_LEFT", "POWER_PILL", "MOVE_RIGHT"]
}
```

### Who is connected

```json
{
  "green": ["joao", "maria"],
  "purple": ["pedro", "ana", "carlos"],
  "spectators": []
}
```

Spectators is for later, in case the room is full and someone wants
to watch instead of play.

### When someone wins

```json
{
  "winner": "green",
  "reason": "score_reached",
  "finalScore": {"green": 10, "purple": 6},
  "duration": 87
}
```

Reason is either `score_reached` (10 food eaten) or
`snake_eliminated` (the other snake reached 0 pixels).
Duration is in seconds.

### The leaderboard

```json
{
  "topScores": [
    {"nickname": "joao", "score": 10, "duration": 65, "date": "2026-05-15"},
    {"nickname": "maria", "score": 10, "duration": 72, "date": "2026-05-14"}
  ]
}
```

---

## Who listens to what

| Component         | Subscribes to                                           |
|-------------------|---------------------------------------------------------|
| Raspberry Pi      | `8x8arena/players/+`, `8x8arena/input/+`                |
| Player browser    | game state, their own hand, players list, winner, leaderboard |
| Spectator (later) | game state, winner, leaderboard                         |

The `+` symbol is a wildcard — `8x8arena/players/+` matches both
`join` and `leave` without me having to subscribe to each one
separately.

---

## Stuff I want to remember

- Match starts when the SenseHAT joystick on the Pi is pressed.
  Before that the LED matrix shows a waiting state.
- The game supports both local console mode and remote mode at the
  same time — same code, different vibe.
- The Pi Camera live feed is what makes remote mode possible.
- The HiveMQ public broker means I don't need to install or configure
  a broker on the Pi. The professor specifically said Mosquitto
  was unreliable, so I'm following his advice.
- All times are Unix timestamps in seconds.
- Only one match running at a time for now. Multiple matches is
  for the next version, if I have time.

---

## Changelog

- **v1.0** — First draft of the topics and message formats.
  Includes player join/leave, card input, game state, private hand,
  player list, winner, and leaderboard. Game starts via SenseHAT
  joystick. Two play modes supported: local console and remote with
  camera stream.
