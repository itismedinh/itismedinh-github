# Import các thư viện cần thiết
import sys
from time import sleep
import json
from urllib import request, parse
from seeed_dht import DHT
import paho.mqtt.client as mqtt
from datetime import datetime
from Lora_Driver_USB.IoT_Driver_USB import LORA_USB

# Cấu hình LoRa USB 
sys.path.append('/home/pi/Desktop/Lora_Driver_USB/')
lora_usb = 8
lora_node = 2
lora = LORA_USB(COM='/dev/ttyUSB0',address=lora_usb)

# Thiết lập client upload dữ liệu lên ThingSpeak thông qua giao thức MQTT 
CHANNEL_ID = '2714697'
CHANNEL_ID_time = '2648594'
USERNAME_UP = 'EBgMGw0bNDssJhs6DjsuMzM'
CLIENTID_UP = 'EBgMGw0bNDssJhs6DjsuMzM'
PASSWORD_UP = 'fZh4CQ2GrRUPnJcFM2nRiDu0'
client_up = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,CLIENTID_UP)
client_up.username_pw_set(USERNAME_UP, PASSWORD_UP)
client_up.connect("mqtt3.thingspeak.com", 1883, 60)
sleep(0.1)

# Thiết lập client download dữ liệu từ ThingSpeak thông qua giao thức MQTT
USERNAME_DOWN = 'AhYeEhY5LhEEBj06JiQYOBI'
CLIENTID_DOWN = 'AhYeEhY5LhEEBj06JiQYOBI'
PASSWORD_DOWN = 'gjTiLFajZOdUE3Aka4iw17Ru'
client_down = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,CLIENTID_DOWN)
client_down.username_pw_set(USERNAME_DOWN, PASSWORD_DOWN)
client_down.connect("mqtt3.thingspeak.com", 1883, 60)
sleep(0.1)

# Tạo payload rỗng
data_send = {}
data_get = {
    'Auto/Manual':0,
    'Den_canh_bao':0,
    'Den_chieu_sang':0,
    'Nhiet_do':0,
    'Do_am':0,
    'Cong_tac_1':0,
    'Cong_tac_2':0,
    'Cong_tac_3':0,
    'Gio_bat_dau':0,
    'Phut_bat_dau':0,
    'Gio_ket_thuc':0,
    'Phut_ket_thuc':0
    }

# Hàm gửi dữ liệu lên ThingSpeak
def send_mqtt(data):
        client_up.publish(f"channels/{CHANNEL_ID}/publish",f"field2={data['Den_canh_bao']}&field3={data['Den_chieu_sang']}&field4={data['Nhiet_do']}&field5={data['Do_am']}&field6={data['Cong_tac_1']}&field7={data['Cong_tac_2']}&field8={data['Cong_tac_3']}&status=MQTTPUBLISH")

# Hàm cho biết response khi kết nối tới server   
def on_connect(client, userdata, flags, rc, properties):
    client.subscribe(f"channels/{CHANNEL_ID}/subscribe")
    client.subscribe(f"channels/{CHANNEL_ID_time}/subscribe")
    print(f"on_connect: {rc}")

# Hàm cho biết response khi ngắt kết nối khỏi server
def on_disconnect (client, userdata, flags, rc, properties):
    print(f"on_disconnect: {rc}")
    
# Hàm trả về dữ liệu khi có thông điệp mới được gửi lên    
def on_message(client, userdata, message):
    data_auto = json.loads(message.payload.decode())
    global data_get
    topic = message.topic

    # Unpack payload để lấy dữ liệu
    if topic == "channels/2714697/subscribe":
        print('topic 1')
        if data_auto.get('field1') is not None:
            data_get['Auto/Manual'] = int(data_auto.get('field1'))
            
        if data_auto.get('field2') is not None:
            data_get['Den_canh_bao'] = int(data_auto.get('field2'))
            
        if data_auto.get('field3') is not None:
            data_get['Den_chieu_sang'] = int(data_auto.get('field3'))
            
        if data_auto.get('field4') is not None:
            data_get['Nhiet_do'] = int(data_auto.get('field4'))
            
        if data_auto.get('field5') is not None:
            data_get['Do_am'] = int(data_auto.get('field5'))
            
        if data_auto.get('field6') is not None:
            data_get['Cong_tac_1'] = int(data_auto.get('field6'))
            
        if data_auto.get('field7') is not None:
            data_get['Cong_tac_2'] = int(data_auto.get('field7'))
            
        if data_auto.get('field8') is not None:
            data_get['Cong_tac_3'] = int(data_auto.get('field8'))

    elif topic == "channels/2648594/subscribe":
        print('topic 2')
        if data_auto.get('field1') is not None:
            data_get['Gio_bat_dau'] = int(data_auto.get('field1'))
            
        if data_auto.get('field2') is not None:
            data_get['Phut_bat_dau'] = int(data_auto.get('field2'))
            
        if data_auto.get('field3') is not None:
            data_get['Gio_ket_thuc'] = int(data_auto.get('field3'))
            
        if data_auto.get('field4') is not None:
            data_get['Phut_ket_thuc'] = int(data_auto.get('field4'))
            
    # Điều khiển đèn dựa trên chế độ auto hoặc manual        
    if data_get['Auto/Manual'] == 0:
        print('Auto')
        now = datetime.now()
        gio_hien_tai = int(now.hour)
        phut_hien_tai = int(now.minute)
        if gio_hien_tai >= data_get['Gio_bat_dau'] and phut_hien_tai >= data_get['Phut_bat_dau']:
            lora.write_data(lora_node,9,1)
            lora.write_data(lora_node,8,1)
        else:
            lora.write_data(lora_node,9,0)
            lora.write_data(lora_node,8,0)
    else:
        print(f"Manual {data_get['Den_chieu_sang']} {data_get['Den_canh_bao']} {data_get['Cong_tac_1']} {data_get['Cong_tac_2']}")
        lora.write_data(lora_node, 8, data_get['Cong_tac_1'])
        lora.write_data(lora_node, 9, data_get['Cong_tac_2'])
    
# Cấu hình lại client   
client_down.on_connect = on_connect
client_down.on_disconnect = on_disconnect
client_down.on_message = on_message

# Cấu hình các chân cảm biến và cho chạy client
dht = DHT('11', 5)
client_down.loop_start()
sleep(0.1)

# Tạo vòng lặp vô hạn để chương trình chạy liên tục
try:
    while 1:
        # Đọc giá trị cảm biến, công tắc và đèn và cho vào payload. 
        data_send['Do_am'], data_send['Nhiet_do'] = dht.read()
        data_send['Cong_tac_1'] = lora.read_data(lora_node, 4)
        data_send['Cong_tac_2'] = lora.read_data(lora_node, 5)
        data_send['Cong_tac_3'] = lora.read_data(lora_node, 6)
        data_send['Den_canh_bao'] = lora.read_data(lora_node, 8)
        data_send['Den_chieu_sang'] = lora.read_data(lora_node, 9)

        print(data_send['Do_am'], data_send['Nhiet_do'])
        # Gửi payload lên server ThingSpeak
        send_mqtt(data_send)
        
    sleep(10)
except KeyboardInterrupt:
    print('Exiting...')
finally:
    client_down.loop_stop()
