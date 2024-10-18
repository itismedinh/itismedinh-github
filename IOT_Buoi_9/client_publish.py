import paho.mqtt.client as mqtt

def on_connect(client, userdata, dlags, rc, porperties):
    client.subscribe('post/')
    print(f"Connected With Result Code: {rc}")

def on_disconnect(client, userdata, flags, rc, properties):
    print("Disconnected From Broker")

def on_message(client, userdata, msg):
    print(f"Received Message: {msg.payload.decode()} on topic {msg.topic}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,'client_read')
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

client.username_pw_set(username='thietbi1',password='thietbi1')
client.connect('127.0.0.1', 1883, 60)

client.loop_forever()