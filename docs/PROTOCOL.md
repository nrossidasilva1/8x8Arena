# 8x8Arena — Communication Protocol

**Version:** 1.1  
**Last updated:** May 2026

How the parts of 8x8Arena talk to each other. If you want to read,
fork, or replace any piece (build your own UI, your own scoreboard,
whatever), the info you need is here.

---

## The Three Parts

- **The Pi** — runs the game, owns the state, drives the LED matrix.
- **The browsers** — players in the lobby and during the match.
- **The MQTT broker** — sits between them.

The Pi and the browsers never talk directly.
   ┌─────────┐         ┌──────────┐         ┌────────┐
   │ Browser │ ◄─────► │  HiveMQ  │ ◄─────► │   Pi   │
   │ (WSS)   │         │  broker  │         │ (TCP)  │
   └─────────┘         └──────────┘         └────────┘
       │                                         │
       │                                         │
   Plays cards                            Drives LED matrix
   Shows grid                             Owns game state
---

## Broker

We use **HiveMQ public broker**, the one the module recommended.
Free, no account, supports TCP and WebSocket Secure (which is what
the browser needs once we're on HTTPS via Netlify). It just worked
for our case.

| Role | Endpoint |
|------|----------|
| Pi (TCP) | `broker.hivemq.com:1883` |
| Browser (WSS) | `wss://broker.hivemq.com:8884/mqtt` |

Public means anyone can subscribe to our topics. Fine for a school
project; for anything real you'd want a private broker.

---

## Why No Pi Camera

v1.0 planned a Pi Camera streaming the LED matrix live to remote
players. We dropped it:

- LED is too bright at close range — the camera sees halos.
- Encoding video on the Pi steals CPU from the game loop.
- The browser would get a fuzzy video of data the Pi already had
  in clean form.

We replaced it with an HTML grid in the browser, fed by the same
state messages that drive the LEDs. Both screens show the same
thing, in sync, no camera needed.

---

## Why No Snake-vs-Snake Collision

v1.0 had a "larger snake beats smaller snake" rule, plus a Power
Pill predator mode where the smaller snake had to physically catch
the larger one's tail. We cut both.

Honest reason: it kept breaking. With two snakes wrapping around
the borders, growing, and overlapping themselves, the collision
logic got tangled fast. Bugs everywhere. With a deadline in sight,
we replaced it with BITE — an instant, deterministic effect — and
shipped.

Collision is on the v2 list when we have time to do it right.

---

## Topics

Everything lives under `8x8arena/`.

### Pi listens to

| Topic | Payload | When |
|-------|---------|------|
| `8x8arena/players/join` | `{"nickname", "team", "timestamp"}` | Player joins from the lobby |
| `8x8arena/input/card` | `{"nickname", "card"}` | Player clicks a card |

### Pi publishes

| Topic | Payload | When |
|-------|---------|------|
| `8x8arena/state/game` | The whole game state | Every tick (0.7s) |
| `8x8arena/state/hand/<nickname>` | `{"nickname", "hand": [4 cards]}` | After join, and after each card played |

Each browser subscribes to its own hand topic
(`8x8arena/state/hand/alice`), not anyone else's.

---

## Card Names

The protocol and the UI use slightly different names:

| Over MQTT | On the card | What it does |
|-----------|-------------|--------------|
| `MOVE_UP` | UP | Up 1 pixel |
| `MOVE_DOWN` | DOWN | Down 1 pixel |
| `MOVE_LEFT` | LEFT | Left 1 pixel |
| `MOVE_RIGHT` | RIGHT | Right 1 pixel |
| `POWER_PILL` | BITE | -2 from opponent's tail |
| `TURBO` | TURBO | 2 px per tick for ~5s |

The browser converts protocol names to display names with a small
map (`PROTOCOL_TO_DISPLAY`).

---

## Game State

This is what gets published on `8x8arena/state/game` every tick:

```json
{
  "game_status": "waiting" | "playing" | "finished",
  "winner": null | "green" | "purple",
  "win_reason": null | "score" | "elimination",
  "victory_shown": false,
  "tick_count": 42,
  "players": {
    "alice": "green",
    "bob": "purple"
  },
  "hands": {
    "alice": ["MOVE_UP", "TURBO", "MOVE_RIGHT", "POWER_PILL"]
  },
  "snakes": {
    "green": {
      "pixels": [[0,0], [1,0], [2,0]],
      "score": 0,
      "direction": "RIGHT",
      "turboActive": false,
      "turboTicks": 0,
      "powerPillActive": false
    },
    "purple": {
      "pixels": [[7,7], [6,7], [5,7]],
      "score": 0,
      "direction": "LEFT",
      "turboActive": false,
      "turboTicks": 0,
      "powerPillActive": false
    }
  },
  "food": [[1,1], [6,6]],
  "pending_cards": {"green": [], "purple": []}
}
```

A few things worth knowing:

- `pixels` is the snake's body. **Last item is the head**, first
  item is the tail.
- Coordinates are `[x, y]`, `(0,0)` top-left, `(7,7)` bottom-right.
- Borders wrap. `x=8` becomes `x=0`.

---

## How a Match Flows

### Joining

1. Browser publishes to `8x8arena/players/join`:
```json
   {"nickname": "alice", "team": "green", "timestamp": 1780000000}
```
2. Pi adds Alice to `players`, draws her a hand of 4, publishes her
   hand to `8x8arena/state/hand/alice`.
3. Browser was already subscribed to its hand topic, renders the
   cards.

### Playing a card

1. Browser publishes to `8x8arena/input/card`:
```json
   {"nickname": "alice", "card": "MOVE_UP"}
```
2. Pi finds Alice's team, puts the card in the team's queue,
   removes that card from Alice's hand, draws a replacement, and
   publishes her updated hand.

### Every tick (0.7s)

The Pi:
1. Picks one card at random from each team's queue (or keeps the
   current direction if the queue is empty).
2. Resolves the card (move, BITE, or TURBO).
3. Handles food and growth.
4. Publishes the new state on `8x8arena/state/game`.

---

## Starting a Match

The match starts from the **SenseHAT joystick** (middle press), not
from any MQTT message. This is on purpose.

8x8Arena is a bridge between the physical world (the Pi sitting on
someone's desk) and the digital world (players in browsers, maybe
across the room, maybe across the planet). The Pi is the **host**.
The browsers are the **players**. The host opens the table, the
players join.

If you want to play, find someone with the Pi and ask them to press
the button. Real-time IoT with a physical handshake.

v2 may add an MQTT start topic for fully remote matches, but the
physical start is part of the v1 concept.

---

## Identity

Whatever nickname the browser sends, the Pi trusts. No login, no
verification. The Pi keeps the `nickname → team` map in
`state["players"]` and uses it to route card plays. A card from a
nickname the Pi doesn't recognize is dropped with a warning.

---

## Building Your Own Client

Since the protocol is just MQTT topics, anyone can write a new
client. A few examples of what's possible:

- A **scoreboard display** on a TV: connect, subscribe to
  `8x8arena/state/game`, render. Done. No need to join.
- A **mobile app** in Flutter or React Native: same as the web
  client, just a different UI.
- A **bot player**: connect, publish a join, subscribe to your own
  hand, publish random cards. Watch chaos unfold.

For a client that just watches (scoreboard, stream overlay):

1. Connect to the broker.
2. Subscribe to `8x8arena/state/game`.

For a full player client:

1. Connect.
2. Subscribe to `8x8arena/state/game`.
3. Publish to `8x8arena/players/join` when the player joins.
4. Subscribe to `8x8arena/state/hand/<nickname>` for their cards.
5. Publish to `8x8arena/input/card` when they play a card.

---

## Changelog

- **v1.1** (May 2026) — Removed Pi Camera; replaced with HTML grid
  in the browser fed by `8x8arena/state/game`. Added BITE card
  (uses the existing `POWER_PILL` identifier on the wire). Cut
  snake-vs-snake collision and predator-mode Power Pill (too
  bug-prone for v1).
- **v1.0** (April 2026) — First protocol draft with Pi Camera video
  stream and MQTT controls.
