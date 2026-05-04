# 8x8Arena — Game Rules

**Game:** Snake Deck Battle
**Version:** 1.0 (initial draft, subject to playtesting)
**Last updated:** May 2026

> Note: rules below are initial hypotheses. Real balancing will only
> happen after the first playtests, so expect this document to evolve
> across versions.

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
- Four players per team (system can scale between 1 and 5).
- Each player has their own private hand of cards on their phone.

---

## Board

The game board is the SenseHAT 8x8 LED matrix.

- The Green snake starts at the top-left corner (0,0).
- The Purple snake starts at the bottom-right corner (7,7).
- Yellow pixels represent food. Two are always present on the board.
- Borders are infinite, like the classic Nokia Snake. A snake exiting
  the right edge appears on the left, exiting the top appears at the
  bottom, and so on.
- Snakes do not die from hitting the border.

---

## Cards

Each player holds four cards at any time, drawn from the team's deck.
There are six card types in total:

| Card           | Effect                                       |
|----------------|----------------------------------------------|
| MOVE UP        | Snake moves 1 pixel up                       |
| MOVE DOWN      | Snake moves 1 pixel down                     |
| MOVE LEFT      | Snake moves 1 pixel left                     |
| MOVE RIGHT     | Snake moves 1 pixel right                    |
| POWER PILL     | Activates predator mode for 5 seconds        |
| TURBO          | Next move advances 2 pixels instead of 1     |

### Deck distribution

- Directional cards: 80% combined (20% each).
- Power Pill: 10% (rare).
- Turbo: 10% (rare).

---

## Turn System

The game loop ticks every one second. On each tick, the system picks
a single card played by the team during that window. If multiple
players from the same team played cards in the same tick, the chosen
card is picked at random — this preserves the chaotic, crowd-controlled
feel of the game. The chosen card moves to the discard pile and
players automatically draw a new card from the deck.

If no player in the team plays a card during a tick window, the snake
does not move on that tick.

---

## Core Mechanics

- Eating yellow food: snake grows by one pixel and the team scores
  one point.
- Hitting your own body: snake shrinks by one pixel.
- Hitting the opponent snake:
  - Larger snake beats smaller snake. The smaller snake shrinks by
    one pixel.
  - If both snakes are the same size, both shrink by one pixel.

---

## Power Pill

Activates predator mode for five seconds. While the effect is active:

- The smaller snake becomes the predator.
- It can eat the last two or three pixels of the larger snake's tail.
  This restriction prevents the smaller snake from abusing the
  mechanic and overgrowing too quickly.
- For each pixel eaten, the larger snake shrinks by one and the
  smaller grows by one.
- Visual indicator: the smaller snake flashes white during the effect.

---

## Turbo

The next snake movement advances two pixels instead of one. Useful
for escaping, reaching food first, or chasing the opponent. The
snake flashes yellow on the next tick as a visual indicator.

---

## Victory Conditions

The first team to achieve any of the following wins the match:

- Reach 10 points (food eaten), or
- Reduce the opponent snake to zero pixels.

---

## Open Balancing Questions

These are knobs to tune during playtesting:

- Tick rate. One second may feel too slow once real network latency
  is added.
- Probability of rare cards (Power Pill and Turbo).
- Length of the "edible tail" during a Power Pill effect.
- Power Pill duration (currently five seconds).
- Initial snake size (one pixel? three?).
- Number of food items on the board (currently two).

---

## Changelog

- **v1.0** — Initial rules draft. Snake mechanics, card system, two
  special cards (Power Pill, Turbo), infinite borders, four players
  per team.
