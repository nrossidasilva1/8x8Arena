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
mqtt_client = None

# MQTT broker config
BROKER_ADDRESS = "broker.hivemq.com"
BROKER_PORT = 1883
TOPIC_STATE_OUT = "8x8arena/state/game"
TOPIC_HAND_PREFIX = "8x8arena/state/hand/"

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
    state["hands"][nickname]= draw_hand(4)
    publish_hand(nickname)
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
    hand = state["hands"].get(nickname, [])
    if card in hand:
        hand.remove(card)
        hand.append(draw_card())
        publish_hand(nickname)
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

# create the both snakes  for the teams game
def process_snake(state, team):    # Process a tick for a single snake (green or purple)
    # get thid team's snake and peding cards
    snake = state["snakes"][team]
    pending = state["pending_cards"][team]

    # decide direction
    if len(pending) == 0:
        direction = snake["direction"]
    else:
        direction = random.choice(pending)
        # only save the move cards no power pills
        if direction in ["UP", "DOWN", "LEFT", "RIGHT"]:
            snake["direction"] = direction
        state["pending_cards"][team] = []
    
    # active turbo car but don't move
    if direction == "TURBO":
        snake["turboActive"] = True
        snake["turboTicks"] = 7
        print(f"{team} Activated TURBO!")
        return
    # habdle BITE (POWER_PILL)
    if direction == "POWER_PILL":
        bite_snake(state, team)
        return

    #  only real direction pass fot the filter
    if direction not in ["UP", "DOWN", "LEFT", "RIGHT"]:
        return
    
    # check the turbo
    if snake["turboActive"]:
        steps = 2
    else:
        steps = 1
    # loop to move the normally or turbo
    for _ in range(steps):
        # calculate new head with wrap-around
        head = snake["pixels"][-1]
        dx, dy = DELTAS[direction]
        new_head = [(head[0] + dx) % BOARD_SIZE, (head[1] + dy) % BOARD_SIZE]
        # check the food colsion , grow and spawn new food
        eaten = check_food_eaten(new_head, state["food"])

        if eaten is not None:
            snake["pixels"] = grow_snake(snake["pixels"], direction)
            state["food"].remove(eaten)
            snake["score"] += 1
            all_snakes = [state["snakes"]["green"]["pixels"], state["snakes"]["purple"]["pixels"]]
            new_food = spawn_food(all_snakes, state["food"], count=1)
            state["food"].extend(new_food)
        else:
            snake["pixels"] = move_snake(snake["pixels"], direction)
    
    # turbo count down
    if snake["turboActive"]:
        snake["turboTicks"] -= 1
        if snake["turboTicks"] <= 0:
            snake["turboActive"] = False
            print(f"{team} turbo gas ended!")

# bite (Power pill) removes 2 from the opponet
def bite_snake(state, team):
    opponent = "purple" if team == "green" else "green"
    opp_pixels = state["snakes"][opponent]["pixels"]
    # remove 2 pixels from tail
    for _ in range(2):
        if len(opp_pixels) > 0:
            opp_pixels.pop(0)

    print (f"{team} BIT {opponent}! Now {len(opp_pixels)} pixels left!")
     # elimination check
    if len(opp_pixels) <= 0:
        state["game_status"] = "finished"
        state["winner"] = team
        state["win_reason"] = "elimination"
        print(f"{team.upper()} WINS by elimination!")

# Check if any team won and update state to finished
def check_victory(state):
    # check if game is currently playing
    if state["game_status"] != "playing":
        return
    # check the teams
    for team in ["green", "purple"]:
        if state["snakes"][team]["score"] >= 10:
            state["game_status"] = "finished"
            state["winner"] = team
            state["win_reason"] = "score"
            print(f"VICTORY! {team.upper()} TEAM WINS!")
            return
 
 # show the winner into the display
def show_victory(state):
    winner = state["winner"]
    if winner == "green":
        color = (0, 255, 0)
    else:
        color = (160, 32, 240)
    
    sense.show_message(f"{winner.upper()}  WINS!", text_colour=color, back_colour=(0, 0, 0))
    sense.clear()
    state["victory_shown"] = True                              

# publish the  current game state as JSON
def publish_state(state):
    # check mqqt client exist
    if mqtt_client is None:
        return
    # convert state to JSON string
    payload = json.dumps(state)
    # publish
    mqtt_client.publish(TOPIC_STATE_OUT, payload)

# publish a player hand via mqtt
def publish_hand(nickname):
    if mqtt_client is None:
        return
    
    hand = state["hands"][nickname]
    topic = TOPIC_HAND_PREFIX + nickname
    payload = json.dumps({
        "nickname": nickname,
        "hand": hand
    })
    mqtt_client.publish(topic, payload)
    print(f"Published hand for {nickname}: {hand}")





# one gametick , both snakes move,check food collision.
def tick(state):
    state["tick_count"] += 1
    if state["game_status"] != "playing":
        return
    process_snake(state,"green")
    process_snake(state,"purple")
    check_victory(state)

 

    

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
    global mqtt_client
    mqtt_client = setup_mqtt()
    print("MQTT connected, listening for players...")
       
    try:
        while True:
            tick(state)
            # if game just finished, show victory message
            if state["game_status"] == "finished" and state["victory_shown"] == False:
                show_victory(state)
            # call the draw_state function to update the LED matrix
            draw_state(state)
            publish_state(state)
            print(f"Tick {state['tick_count']}:")
            print(f"  Green:  {state['snakes']['green']['pixels']}, score={state['snakes']['green']['score']}")
            print(f"  Purple: {state['snakes']['purple']['pixels']}, score={state['snakes']['purple']['score']}")
            time.sleep(0.75)
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