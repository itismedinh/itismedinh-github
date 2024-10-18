import paho.mqtt.client as mqtt
from time import sleep
from random import randint
import json
import urllib

def on_connect(client, userdata, flags, rc, properties):
    print(f"Connected With Result Code: {rc}")

def on_disconnect(client, userdata, flags, rc, properties):
    print("Disconnected From Broker")

def on_message(client, userdata, msg):
    print(f"Received Message: {msg.payload.decode()} on topic {msg.topic}")
    
# def on_publish(client, userdata, mid, rc, properties):
#     client.subscribe('post')
    # client.subscribe('single/read')

# def publish_data(topic, data):
#     if topic == 'single/data':
#         client.publish(topic, json.dumps(data))
#     elif topic == 'all/data':
#         client.publish(topic, urllib.parse.urlencode(data))
    


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,'Raspberry Pi')
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

client.username_pw_set(username='thietbi2',password='thietbi2')
client.connect('127.0.0.1', 1883, 60)

def mqtt_publish(data):
    json_data = json.dumps(data)
    print(json_data)

    client.publish('post',json_data)

while 1:
    data = {
    "temperature": 23.0,
    "humidity": 5.0,
    "led1": randint(0, 1),  
    "led2": randint(0, 1),  
    "led3": randint(0, 1),  
    "device_name": "raspberry"
    }
    # data = 23.0

    mqtt_publish(data)

    sleep(20)