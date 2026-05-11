# import paho
import paho.mqtt.client as mqtt

# broker adress
BROKER_ADDRESS = "broker.hivemq.com"
BROKER_PORT = 1883

# callback function to handle incoming messages
def on_message(client, userdata, message):
    print(f"Topic: {message.topic}, Message: {message.payload.decode('utf-8')}")

# client 
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# register the callback
client.on_message = on_message

# connect to the broker
client.connect(BROKER_ADDRESS, BROKER_PORT)

# subscribe to the topic
client.subscribe("8x8arena/test")

# loop to receive messages
client.loop_forever()
