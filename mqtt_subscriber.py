import paho.mqtt.client as mqtt
import json
import logging
import time 
import requests
from weather_api_request import get_weather_data

mqttBroker = "mqtt.eclipseprojects.io"
topic="TEST"

# Function to handle received messages
def client_side_execution(client, userdata, message):
    # Decode the message payload (assuming JSON)
    data = json.loads(message.payload.decode())
    print ("\ndata in-type ",type(data))
    # Extract desired values
    
    
    # Print the extracted value
    print(f"Received data: {data}")

tunis_latitude = 36.8065
tunis_longitude = 10.1815

# Appelez la fonction pour obtenir les données météorologiques
weather_data_tunis = get_weather_data(tunis_latitude, tunis_longitude)

# Vérifiez si les données ont été obtenues avec succès
if weather_data_tunis:
    print("Weather data for Tunis:")
    print(f"Temperature at 2m: {weather_data_tunis['hourly']['temperature_2m'][0]}°C")
    print(f"Precipitation: {weather_data_tunis['hourly']['precipitation'][0]} mm")
else:
    print("Unable to fetch weather data for Tunis.")


client = mqtt.Client("test1")
client.on_message = client_side_execution
client.connect(mqttBroker)
client.subscribe(topic)
client.loop_forever()

