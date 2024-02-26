import paho.mqtt.client as mqtt
import json
import time

# Define broker address and topic
broker_address = "mqtt.eclipseprojects.io"
topic = "TEST"
counter = 1

# # Sensor functions 
# def read_phSensor():
#     # Read sensor ph data and return a value
#     return 9.5

# def read_ecSensor():
#     # Read sensor ec data and return a value
#     return 20

# # Build JSON data
# data = {
    
#     "sensors": {
#         "phValue": read_phSensor(),
#         "ecValue": read_ecSensor()
#     }
# }

# with open("data.json", "r") as f:
#     data = json.load(f)

def generate_sensor_data():
    global counter
    with open("data.json", "r") as f:
        data = json.load(f)
    counter += 1  # Increment counter before returning
    return data
# Create an MQTT client
client = mqtt.Client()

# Connect to the broker
client.connect(broker_address)

while True:
    # Publish the message every 30 minutes
    data = generate_sensor_data()
    client.publish(topic, json.dumps(data))
    print(f"Published data: {data}, counter: {counter}" )
    print ("\ndata in-type ",type(data))

    time.sleep(1)  # Sleep for 30 minutes (1 seconds)

# Disconnect from the broker (optional, as the script runs indefinitely)
client.disconnect()
