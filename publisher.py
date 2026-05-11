# import the paho mqtt client library
import paho.mqtt.client as mqtt

# define the MQTT broker address and port
BROKER_ADDRESS = "broker.hivemq.com"
BROKER_PORT = 1883

#create the mqtt client instance
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# conect to broker , using BROKER_ADDRESS and BROKER_PORT
client.connect(BROKER_ADDRESS, BROKER_PORT)

# start network loop in background
client.loop_start()


# publish a message to a topic 8x8arena/test
result = client.publish("8x8arena/test", "TEST, MQTT")
result.wait_for_publish()


# disconnect from the broker
client.loop_stop()
client.disconnect()

print("DONE, firsts steps completed")