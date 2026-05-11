from sense_hat import SenseHat
# Import to maintain the program running 
from signal import pause

sense = SenseHat()
# create a function to be called when the button is pressed
def start_button(event): # create the event
    if event.action == 'pressed':  # check if the button is pressed
        print("Start button pressed")  # print a message to the console
        

# set the function when the button is pressed
sense.stick.direction_middle = start_button

# to keep the program running and listen for events
pause()
