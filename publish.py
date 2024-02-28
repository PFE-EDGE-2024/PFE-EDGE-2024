import paho.mqtt.client as mqtt
import json
import time
import os

""" 
import RPI.GPIO as GPIO
GPIO.setmode(gpio.BCM)

GPIO.setup(21,GPIO.IN) #water level sensor 
start_time = time.time()

 """


# broker address and topic
broker_address = "mqtt.eclipseprojects.io"
topic = "Spirulina_Edge"
# values sent by the sensors
Temperature = 50
PH = 15
Water_Level = 10 
Conductivity = 50
Brightness = 11

# Function to read brightness from Endoscope Camera
def read_brightness():
    # Read brightness from Endoscope Camera
    """ camera """
    return Brightness

# Function to read temperature from DS18B20 sensor
def read_temperature():
    # Read temperature from DS18B20 sensor
    """ temperature = ArdTemperatureValue """
    return Temperature

# Function to read pH value from pH sensor
def read_ph():
    # Read pH value from pH sensor (replace with actual sensor reading code)
    """ PH = ArdphValue """
    return PH

# Function to read water level from sensor
def read_water_level():
    # Read water level from sensor (replace with actual sensor reading code)
    """ 
    levelbassin = 25
    capt = GPIO.input(21)
    if capt == 1:
    time_ex = time.time() - start_time
    Water_Level = levelbassin -(time_ex * 0.7)
    """
    return Water_Level

# Function to read conductivity from sensor
def read_conductivity():
    # Read conductivity from sensor (replace with actual sensor reading code)
    """ Conductivity = ArdConductivityValue """
    return Conductivity

# Create an MQTT client
client = mqtt.Client()

# Connect to the broker
client.connect(broker_address)

while True:
    # Read sensor data
    temperature = read_temperature()
    ph_value = read_ph()
    water_level = read_water_level()
    conductivity = read_conductivity()
    brightness  = read_brightness()

    # Construct sensor data dictionary
    sensor_data = {
        "temperature": temperature,
        "pH": ph_value,
        "WaterLevel": water_level,
        "conductivity": conductivity,
        "Brightness" : brightness
    }

    # Construct JSON data
    json_data = {
        "meta": {
           "description": "Contrat JSON pour le projet de bassin de culture de Spiruline"
        },
        "data": {
            "sensors": sensor_data,
        }
    }

    # Write data to JSON file
    with open("sensor_data.json", "w") as json_file:
        json.dump(json_data, json_file, indent=4)

    # Publish the message
    client.publish(topic, json.dumps(json_data))
    print("Published data:", json_data)

    # Sleep for 30 minutes
    time.sleep(30 *60 )

# Disconnect from the broker 
client.disconnect()


""" 
#read code from arduino to raspberry pi 
ser = serial.Serial('"/dev/ttyACM0', 115200)  


# Read data from serial
data = ser.readline().decode().strip()

# Split the data into individual values
ArdphValue, ArdConductivityValue, ArdTemperatureValue = map(float, data.split(","))


        
"""
