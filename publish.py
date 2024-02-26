import paho.mqtt.client as mqtt
import json
import time

# Define broker address and topic
broker_address = "mqtt.eclipseprojects.io"
topic = "TEST"
counter = 0

def generate_sensor_data():
    global counter
    with open("data.json", "r") as f:
        data = json.load(f)
    counter += 1  
    return data
# Create an MQTT client
client = mqtt.Client()

# Connect to the broker
client.connect(broker_address)

while True:
    # Publish the message every 5 minutes
    data = generate_sensor_data()
    client.publish(topic, json.dumps(data))
    print(f"Published data: {data}, counter: {counter}" )
    
    time.sleep(300)  # Sleep 5 minutes

# Disconnect from the broker (optional)
client.disconnect()
