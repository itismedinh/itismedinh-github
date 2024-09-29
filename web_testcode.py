from time import sleep
import paho.mqtt.client as mqtt
from seeed_dht import DHT
from gpiozero import LED, Buzzer
from grove.display.jhd1802 import JHD1802
import json
from datetime import datetime

CHANNEL_ID = '2662258'
USERNAME_UP = 'HigSIxYQARkrMx8WGycXFT0'
CLIENTID_UP = 'HigSIxYQARkrMx8WGycXFT0'
PASSWORD_UP = 'MRCu0aPDU9cBHa2kTfDqOtFn'

USERNAME_DOWN = 'AQgGIRgkKjgqHgIYMxk8Cys'
CLIENTID_DOWN = 'AQgGIRgkKjgqHgIYMxk8Cys'
PASSWORD_DOWN = 'dayHDaPPMW8TaAMYHJqVOD7/'

dht = DHT('11', 26)
buzzer = Buzzer(18)
led = LED(22)
relay = LED(5)
lcd = JHD1802()
data_send = {}
data_get = {
    'Auto/Manual':0,
    'LED':0,
    'Buzzer':0,
    'Relay':0
    }

client_up = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,CLIENTID_UP)
client_up.username_pw_set(USERNAME_UP, PASSWORD_UP)
client_up.connect("mqtt3.thingspeak.com", 1883, 60)
sleep(0.1)

client_down = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,CLIENTID_DOWN)
client_down.username_pw_set(USERNAME_DOWN, PASSWORD_DOWN)
client_down.connect("mqtt3.thingspeak.com", 1883, 60)
sleep(0.1)

def send_mqtt(data):
        client_up.publish(f"channels/{CHANNEL_ID}/publish",f"field5={data['temp']}&field6={data['humi']}&status=MQTTPUBLISH")

def on_connect(client, userdata, flags, rc, properties):
    client.subscribe(f"channels/{CHANNEL_ID}/subscribe")
    print(f"Connected With Result Code: {rc}")

def on_disconnect (client, userdata, flags, rc, properties):
    print(f"Disconnected From Broker: {rc}")
    
def on_message(client, userdata, message):
    data_auto = json.loads(message.payload.decode())
    global data_get
    if data_auto.get('field1') is not None:
        data_get['Auto/Manual'] = int(data_auto.get('field1'))
    if data_auto.get('field2') is not None:
        data_get['LED'] = int(data_auto.get('field2'))
    if data_auto.get('field3') is not None:
        data_get['Buzzer'] = int(data_auto.get('field3'))
    if data_auto.get('field4') is not None:
        data_get['Relay'] = int(data_auto.get('field4'))
    if data_auto.get('field5') is not None:
        data_get['Temp'] = int(data_auto.get('field5'))
    if data_auto.get('field6') is not None:
        data_get['Humi'] = int(data_auto.get('field6'))
        
    if data_get['Auto/Manual'] == 1:
        if data_get['LED'] == 1:
            led.on()
        else:
            led.off()
        if data_get['Relay'] == 1:
            relay.on()
        else:
            relay.off()
        if data_get['Buzzer'] == 1:
            buzzer.on()
        else:
            buzzer.off()
    else:
        hour = datetime.now().hour
        if hour >= 18 and hour <=22:
            led.on()
        else:
            led.off()
        if data_get['Humi'] > 90:
            relay.on()
        elif data_get['Humi'] < 60:
            relay.off()
        if data_get['Temp'] > 37:
            buzzer.on()
        elif data_get['Temp'] < 31:
            buzzer.off()

client_down.on_connect = on_connect
client_down.on_disconnect = on_disconnect
client_down.on_message = on_message

client_down.loop_start()
sleep(0.1)
try:
    while 1:
        date = datetime.now().strftime("%d/%m/%Y")
        time = datetime.now().strftime("%H:%M")
        while 1:
            data_send['humi'], data_send['temp'] = dht.read()
            if data_send['humi'] is not None and data_send['temp'] is not None:
                break
            else:
                continue
        try:  
            send_mqtt(data_send)
        except Exception as e:
            print(f'Error Upload: {e}')
            sleep(1)
        lcd.clear()
        sleep(0.2)
        lcd.setCursor(0,0)
        lcd.write('date: {}'.format(date))
        lcd.setCursor(1,0)
        lcd.write('time: {}'.format(time))
        sleep(20)
        
except KeyboardInterrupt:
    print('Exiting...')
finally:
    client_down.loop_stop()
