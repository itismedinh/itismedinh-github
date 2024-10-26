# Import các thư viện cần thiết, để thực hiện theo yêu cầu đề bài
import paho.mqtt.client as mqtt
from time import sleep
from random import randint
import json
import urllib.parse as parse
from gpiozero import LED
from seeed_dht import DHT

# Cấu hình các chân LED và cảm biến
led1 = LED(22)
sensor = DHT("11", 5)

# Hàm callback khi kết nối thành công với broker để biết nếu ta đã kết nối hay chưa
def on_connect(client, userdata, flags, rc, properties):
    print(f"Connected With Result Code: {rc}")

# Hàm callback khi ngắt kết nối với broker để biết ta đã ngắt kết nối với broker
def on_disconnect(client, userdata, flags, rc, properties):
    print("Disconnected From Broker")

# Hàm callback khi có message từ broker, để biết khi nào có message
def on_message(client, userdata, msg):
    print(f"Message Received")

# Khởi tạo client MQTT
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,'Raspberry Pi')
client.on_connect = on_connect
client.on_disconnect = on_disconnect    
client.on_message = on_message

# Cài đặt user và thực hiện kết nối với broker
client.username_pw_set(username='thietbi2',password='thietbi2')
client.connect('192.168.1.167', 1883, 60)

# Hàm publish dữ liệu dưới dạng json
def send_all_json(data):
    json_data = json.dumps(data)
    print(f'Json Data: {json_data}')
    client.publish("post_all_json",json_data)

# Hàm publish dữ liệu dưới dạng url
def send_all_url(data):
    urlencoded_data = parse.urlencode(data)
    print(f"Form Data: {urlencoded_data}")
    client.publish("post_all_url", urlencoded_data)

# Ta tạo vòng lặp vô hạn để chương trình chạy liên tục
while True:
    # Ở đây ta đọc giá trị cảm biến và đóng gói dữ liệu
    humid, temp = sensor.read()
    data = {
        "temperature": temp,
        "humidity": humid,
        "led1": randint(0, 1),
        "device_name": "raspberry"
    }
    # Điều khiển LED dựa trên giá trị ngẫu nhiên
    led1.on() if data['led1'] else led1.off()
    # Gửi dữ liệu lên broker
    send_all_json(data)
    sleep(5)
    send_all_url(data)
    sleep(5)
