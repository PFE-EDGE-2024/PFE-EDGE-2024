import paho.mqtt.client as mqtt
import json
import logging
import time 
import requests
from weather_api import get_weather_data

# MQTT Broker configuration
mqttBroker = "mqtt.eclipseprojects.io"
topic = "Spirulina_Edge"

tunis_latitude = 36.8065
tunis_longitude = 10.1815

# Function to handle received messages
def client_side_execution(client, userdata, message):
    # Decode the message payload (assuming JSON)
    data = json.loads(message.payload.decode())
    # Extract sensor data
    sensors_data  = data.get('data', {}).get('sensors', {})
    # Fetch weather data
    weather_data_tunis = get_weather_data(tunis_latitude, tunis_longitude)
    # Check if weather data is available
    if weather_data_tunis:
        # Augment JSON data with weather variables
        #sensors_data['temperature'] = weather_data_tunis['hourly']['temperature_2m'][0]
        # Print the updated data
        print("Received sensor data with weather variables:")
        # Print sensor data
        print(f"Temperature: {sensors_data.get('temperature')} °C")
        print(f"pH: {sensors_data.get('pH')} pH")
        print(f"Water Level: {sensors_data.get('WaterLevel')} cm")
        print(f"Conductivity: {sensors_data.get('conductivity')} µS/cm")
        print(f"Brightness: {sensors_data.get('Brightness')} lm")
        # Determine weather condition
        weather_condition = determine_weather_condition(weather_data_tunis)
        print(f"Weather Temperature: {weather_data_tunis['hourly']['temperature_2m'][0]} °C")
        print(f"Weather Condition: {weather_condition}")
        make_recommendations(weather_condition, sensors_data)
    else:
        print("Unable to fetch weather data.")


# Function to determine weather condition
def determine_weather_condition(weather_data):
    # Extract relevant weather parameters
    weather_temperature = weather_data['hourly']['temperature_2m'][0]
    precipitation = weather_data['hourly']['precipitation'][0]
    # Check weather conditions
    if precipitation > 0:
        return "Raining"
    elif weather_temperature > 25:
        return "Sunny"
    else:
        return "windy"
    

def make_recommendations(weather_condition, sensor_data):
    recommendations = []
    #ph recommendation
    ph = sensor_data.get('pH' , None)
    if ph is not None:
        if ph > 11:
            recommendations.append("Add Bicarbonate to decrease pH")
    #water_level recommandation
    water_level = sensor_data.get('WaterLevel', None)
    if water_level is not None:
        recommendations.append(f"Water level: {water_level} (check if within desired range)")
    #brightness recommendation
    brightness = sensor_data.get('Brightness', None)
    if brightness is not None:
        if 2 <= brightness <= 10:
            recommendations.append("Brightness within optimal range")
        elif brightness > 10:
            recommendations.append("Add Nitrate to decrease density")
    #salinity recommendation
    salinity = sensor_data.get('conductivity', None)
    if salinity is not None:
        if 15 <= salinity <= 40:
            recommendations.append("Salinity within optimal range")
        elif salinity < 15:
            recommendations.append("Add salt to increase salinity")
        elif salinity > 40 :
            recommendations.append("Add water to decrease salinity")
        elif salinity > 40 and weather_condition == 'Raining':
            recommendations.append("it's raining no need to add water")
    for recommendation in recommendations:
        print("Recommendations:" + recommendation)
       
   

# Callback function when connection to MQTT broker is established
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker with result code "+str(rc))
    # Subscribe to topic
    client.subscribe(topic)


# Create MQTT client
client = mqtt.Client(topic)

# Set callback functions
client.on_message = client_side_execution
client.on_connect = on_connect

# Connect to MQTT broker
client.connect(mqttBroker)

# Run MQTT client loop
client.loop_forever()
