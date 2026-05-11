from sense_hat import SenseHat
import time

# create an instance of the SenseHat
sense = SenseHat()

# set snake head color green from de parameter 0,0 to 3,0  only one time (test)
sense.set_pixel(0, 0, 0, 255, 0)
sense.set_pixel(1, 0, 0, 255, 0)
sense.set_pixel(2, 0, 0, 255, 0)

time.sleep(3)
# off the led
sense.clear()
