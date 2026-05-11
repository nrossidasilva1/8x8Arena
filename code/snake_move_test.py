from sense_hat import SenseHat
import time 

# instance SenseHat
sense = SenseHat()

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
# off the led and close the loop
sense.clear()

