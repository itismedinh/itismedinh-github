# Chúng ta cần giao tiếp với các ngoại vi và giao thức mqtt nên cần các thư viện sau
from time import sleep
import paho.mqtt.client as mqtt
from seeed_dht import DHT
from gpiozero import LED, Buzzer
from grove.display.jhd1802 import JHD1802
import json
from datetime import datetime

# Khai báo các ID, tài khoản mqtt để gửi và nhận dữ liệu với server thingspeak
CHANNEL_ID = '2662258'
USERNAME_UP = 'HigSIxYQARkrMx8WGycXFT0'
CLIENTID_UP = 'HigSIxYQARkrMx8WGycXFT0'
PASSWORD_UP = 'MRCu0aPDU9cBHa2kTfDqOtFn'
USERNAME_DOWN = 'KRUjDjMsOBsxOicCIz0AJSY'
CLIENTID_DOWN = 'KRUjDjMsOBsxOicCIz0AJSY'
PASSWORD_DOWN = '0M8IgvKk6VQlKfN4gmxKSzGF'
# Khai báo cho các thiết bị cần sử dụng theo đề bài
dht = DHT('11', 26)
buzzer = Buzzer(18)
led = LED(22)
relay = LED(5)
lcd = JHD1802()

# Khai báo 2 dic để lưu trữ dữ liệu gửi và nhận
data_send = {}
data_get = {
    'Auto/Manual':0,
    'LED':0,
    'Buzzer':0,
    'Relay':0
    }

# Thiết lập các tài khoản gửi và nhận dữ liệu mqtt 
client_up = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,CLIENTID_UP)
client_up.username_pw_set(USERNAME_UP, PASSWORD_UP)
client_up.connect("mqtt3.thingspeak.com", 1883, 60)
sleep(0.1)

client_down = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,CLIENTID_DOWN)
client_down.username_pw_set(USERNAME_DOWN, PASSWORD_DOWN)
client_down.connect("mqtt3.thingspeak.com", 1883, 60)
sleep(0.1)

# Ta cần dòng code sau vì cần gửi dữ liệu lên thingspeak theo giao thức mqtt
def send_mqtt(data):
        client_up.publish(f"channels/{CHANNEL_ID}/publish",f"field5={data['temp']}&field6={data['humi']}&status=MQTTPUBLISH")

# Ta cần thiết lập các hàm để xử lý các sự kiện trong trong giao thức mqtt
def on_connect(client, userdata, flags, rc, properties):
    client.subscribe(f"channels/{CHANNEL_ID}/subscribe")
    print(f"Connected With Result Code: {rc}")

def on_disconnect (client, userdata, flags, rc, properties):
    print(f"Disconnected From Broker: {rc}")
    
def on_message(client, userdata, message):
    data_auto = json.loads(message.payload.decode())
    global data_get
    # Ta cần xử lý data trước khi gán dữ liệu vì không phải lúc nào cũng có data
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
    # Thiết lập các chế độ điều khiển theo đề bài
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
        elif data_get['LED'] == 1:
            led.off()
        if data_get['Humi'] > 90:
            relay.on()
        elif data_get['Humi'] < 60:
            relay.off()
        if data_get['Temp'] > 37:
            buzzer.on()
        elif data_get['Temp'] < 31:
            buzzer.off()
# Liên kết các hàm để xử lý sự kiện với client mqtt
client_down.on_connect = on_connect
client_down.on_disconnect = on_disconnect
client_down.on_message = on_message
# Khởi động một vòng lặp chạy ngầm trong nền để xử lý kết nối và nhận dữ liệu từ broker mqtt một cách tự động
client_down.loop_start()
sleep(0.1) # Tạo delay để đảm bảo các thiết lập được xử lý hoàn tất
try: # Ta cần cấu trúc try-except-finally để đảm bảo chương trình chạy đúng theo yêu cầu
    while 1:
        # Ta cần lấy thời gian để hiển thị lcd theo yêu cầu đề bài
        date = datetime.now().strftime("%d/%m/%Y")
        time = datetime.now().strftime("%H:%M")
        # Ta cần đọc và xử lý lỗi cảm biến
        data_send['humi'], data_send['temp'] = dht.read()
        while (data_send['humi'] < 10 or data_send['humi'] > 100) or (data_send['temp'] < 20 or data_send['temp'] > 70):
            data_send['humi'], data_send['temp'] = dht.read()
            sleep(1)
        # Ta cần các dòng code sau để đảm bảo nếu có lỗi trong quá trình gửi dữ liệu thì chương trình sẽ không bị dừng lại
        try:  
            send_mqtt(data_send)
        except Exception as e:
            print(f'Error Upload: {e}')
            sleep(1)
        # Ta cần các dòng code sau để hiển thị thời gian ra lcd theo đề bài
        lcd.clear()
        sleep(0.2)
        lcd.setCursor(0,0)
        lcd.write('date: {}'.format(date))
        lcd.setCursor(1,0)
        lcd.write('time: {}'.format(time))
        sleep(20)
# Ta cần các dòng code sau vì nếu cần dừng chương trình, chương trình sẽ đóng kết nối một cách an toàn
except KeyboardInterrupt:
    print('Exiting...')
finally:
    client_down.loop_stop()
