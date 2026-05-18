# import all the functions for the game 
from state import make_waiting_state
from snake import move_snake, grow_snake
from food import spawn_food, check_food_eaten
from deck import draw_card, draw_hand
from display import draw_state
from snake import DELTAS, BOARD_SIZE
# import the standed libraries and sense hat
from sense_hat import SenseHat
import random
import time
import json
import paho.mqtt.client as mqtt


# create a inicial state
sense = SenseHat()
state = make_waiting_state()

# MQTT broker config
BROKER_ADDRESS = "broker.hivemq.com"
BROKER_PORT = 1883

# Map MQTT card names to internal direction strings
CARD_TO_DIRECTION = {
    "MOVE_UP": "UP",
    "MOVE_DOWN": "DOWN",
    "MOVE_LEFT": "LEFT",
    "MOVE_RIGHT": "RIGHT",
    "POWER_PILL": "POWER_PILL",
    "TURBO": "TURBO"
}

def handle_join(client, userdata, message):
    """Callback when the player join"""
    payload = json.loads(message.payload.decode("utf-8"))
    nickname = payload["nickname"]
    team = payload["team"]

    #find the player's team
    state["players"][nickname] = team
    print(f"Player joined: {nickname}({team})")

# Callback form the cards played 
def handle_cards(client, userdata, message):
    payload = json.loads(message.payload.decode("utf-8"))
    nickname = payload["nickname"]
    card = payload["card"]

    #find the player's team 
    if nickname not in state["players"]:
        print(f"Unknown player: {nickname}, ignoring card")
        return
    team = state["players"][nickname]

    # convert card name to direction
    direction= CARD_TO_DIRECTION.get(card, None)
    if direction is None:
        print(f"Unknown card: {card}")
        return

    # add the card to the queue
    state["pending_cards"][team].append(direction)
    print(f"Card form {nickname} ({team}): {card}  → {direction}")

def setup_mqtt():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.message_callback_add("8x8arena/players/join", handle_join)
    client.message_callback_add("8x8arena/input/card", handle_cards)
    client.connect(BROKER_ADDRESS, BROKER_PORT)
    client.subscribe("8x8arena/players/join")
    client.subscribe("8x8arena/input/card")
    client.loop_start()
    return client

# process game tick: move green snake , check food collsion 
def tick(state):
    state["tick_count"] += 1
    # only rappens if the game is "playing"
    if state ["game_status"] != "playing":
        return
    green = state["snakes"]["green"]
    pending = state["pending_cards"]["green"]
    
    #decide direction
    if len(pending) == 0:
        # queue is empty : use the actual direction
        direction = green["direction"]
    else: 
        # queue is not empty : shuffle and use a card
        direction = random.choice(pending)
        green["direction"] = direction
        #clean the queue
        state["pending_cards"]["green"] = [] 

    # filter the direction
    if direction not in ["UP", "DOWN", "LEFT", "RIGHT"]:
        return

    # calculate new head position
    head = green["pixels"][-1]
    dx, dy = DELTAS[direction]
    new_head = [(head[0] + dx) % BOARD_SIZE, (head[1] + dy) % BOARD_SIZE]

    # check if the food is at new head position
    if new_head in state["food"]:
        # Grow
        green["pixels"] = grow_snake(green["pixels"], direction)
        # Remove food
        state["food"].remove(new_head)
        # score up
        green["score"] += 1
        # spawn new food
        all_snakes = [state["snakes"]["green"]["pixels"], state["snakes"]["purple"]["pixels"]]
        new_food = spawn_food(all_snakes, state["food"], count=1)
        state["food"].extend(new_food)
    else:
        # Move
        green["pixels"] = move_snake(green["pixels"], direction)

    

# add joystick middle to start/ restart match   
def start_button(event):
    global state
    if event.action != 'pressed':
        return
    if state["game_status"] == "waiting":
        state["game_status"] = "playing"
        print("Match started!")

    elif state["game_status"] == "finished":
        state = make_waiting_state()
        print("Match reset - waiting for new start")

    else:
        print("Match already in progress!")

def main():
    print("8x8 Arena starting...")
    print(f"Initial state loaded: game_status = {state['game_status']}")
    # the callback joystick
    sense.stick.direction_middle = start_button
    mqtt_client = setup_mqtt()
    print("MQTT connected, listening for players...")

   
    try:
        while True:
            tick(state)
            # call the draw_state function to update the LED matrix
            draw_state(state)
            print(f"Tick {state['tick_count']}: green at {state['snakes']['green']['pixels']}, score={state['snakes']['green']['score']}")
            time.sleep(1)
            # update the state
            
    except KeyboardInterrupt:
        print("\nShutting down... ")
    finally:
        sense.clear()
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
        print("Cleaned up. Bye.")

if __name__ == "__main__":
    main()