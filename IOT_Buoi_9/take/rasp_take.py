import paho.mqtt.client as mqtt
from time import sleep
from random import randint
import json
import urllib.parse as parse
from gpiozero import LED
from seeed_dht import DHT

led1 = LED(22)
sensor = DHT("11", 5)

def on_connect(client, userdata, flags, rc, properties):
    print(f"Connected With Result Code: {rc}")

def on_disconnect(client, userdata, flags, rc, properties):
    print("Disconnected From Broker")

def on_message(client, userdata, msg):
    print(f"Message Received")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,'Raspberry Pi')
client.on_connect = on_connect
client.on_disconnect = on_disconnect    
client.on_message = on_message

client.username_pw_set(username='thietbi2',password='thietbi2')
client.connect('192.168.1.167', 1883, 60)

def send_all_json(data):
    json_data = json.dumps(data)
    print(f'Json Data: {json_data}')
    client.publish("post_all_json",json_data)

def send_all_url(data):
    urlencoded_data = parse.urlencode(data)
    print(f"Form Data: {urlencoded_data}")
    client.publish("post_all_url", urlencoded_data)

while True:
    humid, temp = sensor.read()
    data = {
        "temperature": temp,
        "humidity": humid,
        "led1": randint(0, 1),
        "device_name": "raspberry"
    }
    
    led1.on() if data['led1'] else led1.off()

    send_all_json(data)
    sleep(5)
    send_all_url(data)
    sleep(5)
