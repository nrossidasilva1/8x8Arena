from sense_hat import SenseHat
import time 
# create an instance of the SenseHat 
sense = SenseHat()

# set the color of the parametr x4,y4 to blue
sense.set_pixel(4, 4, 0, 0, 255)

# freeze time for 3 seconds
time.sleep(3)

# off the led 
sense.clear()

