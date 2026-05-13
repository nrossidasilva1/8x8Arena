# import libraries
from sense_hat import SenseHat 
import time

#create variables
game_state = "waiting" 
tick_count = 0
sense = SenseHat()

# Call back of joystick button 
def start_button(event):
    if event.action == 'pressed':
        global game_state

        # if we are in waiting turn to playing
        if game_state == 'waiting':
            game_state = 'playing'
            print("Match started!")
            
            
        # next match finish to waiting
        elif game_state == 'finished':
            game_state = 'waiting'
            print("Waiting for the next match...")
        
        # playing 
        else:
            print("Match already in progress!")

# register the callback joystick
sense.stick.direction_middle = start_button       

    

# main loop
try:
    while True:
        tick_count += 1
        print(f"Tick: {tick_count}, Game State: {game_state}")
        time.sleep(1)   # to slow down the loop for test

except KeyboardInterrupt:
    print("\nShutting down...")

finally:
    print(f"Tick: {tick_count} , state: {game_state}")