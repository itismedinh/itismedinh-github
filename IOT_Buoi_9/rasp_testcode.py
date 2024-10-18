import paho.mqtt.client as mqtt
from time import sleep
from random import randint
import json
import urllib.parse as parse

def on_connect(client, userdata, flags, rc, properties):
    print(f"Connected With Result Code: {rc}")

def on_disconnect(client, userdata, flags, rc, properties):
    print("Disconnected From Broker")

def on_message(client, userdata, msg):
    print(f"Message Received")

def on_publish(client, userdata, mid):
    print(f"Message published with mid: {mid}")
    client.subscribe("post_temp_json")
    client.subscribe("post_humi_json")
    client.subscribe("post_led1_json")
    client.subscribe("post_led2_json")
    client.subscribe("post_led3_json")
    client.subscribe("post_all_json")
    client.subscribe("post_all_url")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,'Raspberry Pi')
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.on_publish = on_publish

client.username_pw_set(username='thietbi2',password='thietbi2')
client.connect('127.0.0.1', 1883, 60)

def send_all_json(data):
    json_data = json.dumps(data)
    print(f'Json Data: {json_data}')
    client.publish("post",json_data)

def send_all_url(data):
    urlencoded_data = parse.urlencode(data)
    print(f"Form Data: {urlencoded_data}")
    client.publish("post_all_url", urlencoded_data)

def send_temp_json(data):
    mydict = {
        "temperature": data["temperature"],
        "device_name": data["device_name"]
    }
    json_data = json.dumps(mydict)
    print(json_data)
    client.publish("post_temp",json_data)

def send_humi_json(data):
    mydict = {
        "humidity": data["humidity"],
        "device_name": data["device_name"]
    }
    json_data = json.dumps(mydict)
    print(json_data)
    client.publish("post_humi",json_data)

def send_led1_json(data):
    mydict = {
        "led1": data["led1"],
        "device_name": data["device_name"]
    }
    json_data = json.dumps(mydict)
    print(json_data)
    client.publish("post_led1",json_data)

def send_led2_json(data):
    mydict = {
        "led2": data["led2"],
        "device_name": data["device_name"]
    }
    json_data = json.dumps(mydict)
    print(json_data)
    client.publish("post_led2",json_data)

def send_led3_json(data):
    mydict = {
        "led3": data["led3"],
        "device_name": data["device_name"]
    }
    json_data = json.dumps(mydict)
    print(json_data)
    client.publish("post_led3",json_data)

while True:
    data = {
        "temperature": 23.0,
        "humidity": 5.0,
        "led1": randint(0, 1),
        "led2": randint(0, 1),
        "led3": randint(0, 1),
        "device_name": "raspberry"
    }

    # send_all_json(data)
    # sleep(5)
    send_all_url(data)
    sleep(5)
    break
    # send_temp_json(data)
    # sleep(5)
    # send_humi_json(data)
    # sleep(5)
    # send_led1_json(data)
    # sleep(5)
    # send_led2_json(data)
    # sleep(5)
    # send_led3_json(data)
    # sleep(5)

    # sleep(20)