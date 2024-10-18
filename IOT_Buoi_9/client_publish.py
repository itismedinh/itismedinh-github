#Import thư viện MQTT
import paho.mqtt.client as mqtt

# Hàm đăng kí tới broker khi kết nối thành công
def on_connect(client, userdata, dlags, rc, porperties):
    client.subscribe('post/')
    print(f"Connected With Result Code: {rc}")

# Hàm huỷ đăng kí tới broker khi ngừng kết nối
def on_disconnect(client, userdata, flags, rc, properties):
    print("Disconnected From Broker")

# Hàm hiển thị thông điệp từ topic được đăng kí khi có thông điệp mới 
def on_message(client, userdata, msg):
    print(f"Received Message: {msg.payload.decode()} on topic {msg.topic}")

# Tạo một client mới
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,'client_read')

# Gắn các sự kiện cho client
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

# Cấu hình thông tin người dùng và mật khẩu để xác thực với broker và bắt đầu kết nối 
client.username_pw_set(username='thietbi1',password='thietbi1')
client.connect('127.0.0.1', 1883, 60)

# Cho client lắng nghe liên tục cho đến khi có tín hiệu dừng 
client.loop_forever()