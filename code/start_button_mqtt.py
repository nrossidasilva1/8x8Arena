# import  libraries
from sense_hat import SenseHat
import paho.mqtt.client as mqtt
from signal import pause

# broker config
BROKER_ADDRESS = "broker.hivemq.com"
BROKER_PORT = 1883

# create mqtt client instance , conect and start the loop
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(BROKER_ADDRESS, BROKER_PORT)
client.loop_start()

# sense hat creation
sense = SenseHat()

# callback of the joystick button
def start_button(event):
    if event.action == "pressed":
        print("Match start!")
        client.publish("8x8arena/game/start", "Match start!")


# register the callback
sense.stick.direction_middle = start_button

# keep working until the user stop
pause()