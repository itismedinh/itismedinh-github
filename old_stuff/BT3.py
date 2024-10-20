# Trong bài này chúng ta sử dụng các cảm biến DHT11, cảm biến nhiệt độ, cảm biến ánh sáng và LCD để tải lên ThingSpeak sử dụng các phuơng thức HTTP và MQTT  
from time import sleep
from urllib import request, parse
import paho.mqtt.client as mqtt
from seeed_dht import DHT
from grove.grove_light_sensor_v1_2 import GroveLightSensor
from grove.display.jhd1802 import JHD1802
from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger

# Thiết lập key API nhận cho phương thức HTTP và user cho phương thức MQTT 
HTTP_API_KEY = 'AG0NMH46GW86GGDZ'
MQTT_USERNAME = 'Ohg3DioQMjclJQ4TDQQVBSI'
MQTT_PASSWORD = 'TQVxCu87QTriJVtoKJy/VM8J'
MQTT_CLIENT_ID = 'Ohg3DioQMjclJQ4TDQQVBSI'
MQTT_CHANNEL_ID = '2648596'

# Hàm send_http để đóng gói các dữ liệu và gửi lên server bằng phương thức HTTP
def send_http(data):
    url = 'https://api.thingspeak.com/update'
    params = parse.urlencode({
        'field1': data['temp'],
        'field2': data['humi'],
        'field3': data['distance'],
        'field4': data['light']
    }).encode()
    req = request.Request(url, data=params, method='POST')
    req.add_header('Content-Type', 'application/x-www-form-urlencoded')
    req.add_header('X-THINGSPEAKAPIKEY', HTTP_API_KEY)
    response = request.urlopen(req)
    return response.read()

# Hàm send_http để đóng gói các dữ liệu và gửi lên server bằng phương thức HTTP
def send_mqtt(client, data):
    payload = f"field1={data['temp']}&field2={data['humi']}&field3={data['distance']}&field4={data['light']}&status=MQTTPUBLISH"
    topic = f"channels/{MQTT_CHANNEL_ID}/publish"
    client.publish(topic, payload)

# Thực hiện kết nối với server bằng MQTT 
client = mqtt.Client(MQTT_CLIENT_ID)
client.username_pw_set(username=MQTT_USERNAME, password=MQTT_PASSWORD)
client.connect("mqtt3.thingspeak.com", 1883, 60)

# Nối DHT vào chân D5, cảm biến khoảng cách vào chân D22, cảm biến ánh sáng vào chân A0, LCD vào chân I2C  
dht = DHT('11', 5)
ultra = GroveUltrasonicRanger(22)
light = GroveLightSensor(0)
lcd = JHD1802()

# Tiến hành gửi dữ liệu lên server ThinkSpeak liên tục mỗi 20s và in lên LCD
while 1:
    while 1:
        humi, temp = dht.read()
        distance = ultra.get_distance()
        light_level = light.light

        # Kiểm tra dữ liệu bất thường
        if humi <= 0:
            print('humi error')
        elif(temp <= 0):
            print('temp error')
        elif(distance <= 0):
            print('distance error')
        elif(light_level <= 0):
            print('light error')
        else:
            break
       
    lcd.clear()
    sleep(0.5)
    lcd.setCursor(0, 0)
    lcd.write(f'{temp}c      {humi}%')
    lcd.setCursor(1, 0)
    lcd.write(f'{distance:.1f}cm   {light_level}')

    sensor_data = {
        'temp': temp,
        'humi': humi,
        'distance': distance,
        'light': light_level
    }

    # Kiểm tra kết nối có bị gián đoạn hay không
    try:
        send_http(sensor_data)
    except Exception as error:
        print(f'Error HTTP: {error}')
        sleep(1)
    try:
        send_mqtt(client, sensor_data)
    except Exception as error:
        print(f'Error MQTT: {error}')
        sleep(1)

    sleep(20)


