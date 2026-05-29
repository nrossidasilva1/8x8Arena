# 8x8Arena — Game Rules

**Game:** Snake Deck Battle  
**Version:** 1.1  
**Last updated:** May 2026

> These rules describe v1.1 — the version actually shipped. v1.0 was
> a paper design (predator-mode Power Pill, snake collision, 1-second
> ticks) but most of it didn't survive contact with playtesting and
> Pi hardware.

---

## Concept

8x8Arena is a crowd-controlled twist on the classic Snake game. Two
teams compete on a shared 8x8 LED matrix (the SenseHAT), but instead
of pressing keys, players play cards from their hand on their phones
to control the team's snake. The deck mechanic adds a layer of
strategy on top of the chaotic "Twitch Plays" style multiplayer.

---

## Teams

- Two teams: Green and Purple.
- Each team controls one snake on the board.
- Each player holds 4 cards.
- Each player has their own private hand of cards on their phone.

---

## How to Play

Open the lobby, type a nickname, pick a team. You'll see the arena
and four cards in your hand. Tap a card — it joins your team's
queue. The game doesn't wait for you, it just keeps ticking. When a
tick happens, your team's queue gets shuffled and one card wins. The
snake moves accordingly.

If nobody on your team played anything that tick, the snake just
keeps going wherever it was already heading. Like the original Nokia
Snake. It doesn't stop and wait for you.

---

## Board (The Arena)

The board is **8x8**, mirrored in two places at once:

- The physical SenseHAT LED matrix (the real game)
- An HTML grid in the browser (live mirror, fed by the same MQTT
  state stream)

Borders **wrap around** — walk off the right edge, you come out the
left. Top wraps to bottom. The board is a torus.

---

## The Cards

You hold four at a time. Once you play one, a new card is drawn to
replace it.

**Direction cards** — UP, DOWN, LEFT, RIGHT. Move the snake one
pixel. These are the bread and butter, most of your hand will look
like this.

**TURBO** — your snake moves two pixels per tick instead of one, for
about five seconds. Useful for catching up to food or escaping a
BITE.

**BITE** (`POWER_PILL` in the protocol) — chomps two pixels off the
opponent's tail. Instant. No aiming, no contact required. Just
delete two of their cells. Stack enough of these and the opponent
disappears entirely.

### Deck distribution

- Directional cards: 80% combined (20% each).
- BITE: 10% (rare).
- TURBO: 10% (rare).

---

## Turn System

The game ticks every **0.7 seconds**. On each tick:

- One card is picked at random from each team's queue.
- The card resolves (move, BITE, or TURBO).
- If the queue is empty, the snake keeps going in its current
  direction.

---

## Core Mechanics

Eating yellow food: snake grows by one pixel and the team scores one
point. A new food spawns somewhere else on the board.

---

## Victory Conditions

The first team to achieve any of the following wins the match:

- Reach **10 points** (food eaten), or
- Reduce the opponent snake to **0 pixels** via BITE.

When a team wins, the SenseHAT displays a victory message in the
winning team's color, and the browser shows an animated banner. The
match (timestamp, winner, scores, and player nicknames per team) is
saved to `leaderboard.csv` for the match history.

---

## Starting and Resetting

Press the **middle button on the SenseHAT joystick** to start a
match. Press it again after someone wins to reset and let new
players join.

---

## What It Doesn't Have (Yet)

Snakes pass through each other. There's no self-collision either —
a snake can fold onto itself without dying. The only way to shorten
an opponent is BITE.

The truth: v1.0 had collision and a predator mode for Power Pill,
but the logic kept breaking once snakes wrapped around borders,
overlapped, and grew. With a deadline coming, we cut both and
shipped BITE instead (instant, deterministic, hard to break).
Proper collision is on the v2 list.

Planned for v2:

- Snake-vs-snake collision
- Self-collision
- Minimum-player check before starting
- Chat, sound, CPU opponent
- Leaderboard display page (currently only the CSV exists)