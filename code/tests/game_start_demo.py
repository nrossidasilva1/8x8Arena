from sense_hat import SenseHat
import time 


sense = SenseHat()
game_started = False

# animation for the start
def show_intro():
    """Colors waterfall from the button to the top + text '8x8 ARENA'"""
    colors = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 255, 0), (0, 255, 255), (0, 0, 255), (128, 0, 128), (255, 0, 255)]
    for y in range(7, -1, -1):
        for x in range(8):
            sense.set_pixel(x, y, colors[y])
        time.sleep(0.10)

    time.sleep(1)
    sense.clear()

    # Display "8x8 ARENA" text
    sense.show_message("8x8 ARENA", text_colour= (255, 0, 0,), back_colour=(25, 25, 112), scroll_speed=0.08)
    sense.clear()

 # callback to joystick
def start_game(event):
    if event.action == 'pressed':
        global game_started
        game_started = True
        print("Match started!")

# snake animation
def run_snake_demo():
    """Snake draws + 20 interactions of movent wihth wraparound"""
    # snake head in the starting position
    sense.set_pixel(0, 0, 0, 255, 0)
    sense.set_pixel(1, 0, 0, 255, 0)
    sense.set_pixel(2, 0, 0, 255, 0)
    time.sleep(1)

    # move the snake to the right three times using loop >> displacement
    for i in range(20): # loop to move in the infity board
       sense.set_pixel(i % 8, 0, 0, 0, 0) # set the new head position
       sense.set_pixel((i + 3) % 8, 0, 0, 255, 0) # wrap around the board using modulo operator
       time.sleep(1) # delay to see the movement

# Callback registration
sense.stick.direction_middle = start_game

#main loop
try:
    show_intro()
    
    while True:
        if game_started:
            run_snake_demo()
            game_started = False # reset after demo
        time.sleep(0.1) # pause to not fried the CPU

except KeyboardInterrupt:
    print("\nShutting down...")
    
finally:
    sense.clear()
    print("Leds OFF")
