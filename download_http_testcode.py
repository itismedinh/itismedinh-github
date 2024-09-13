from time import sleep
from urllib import request, parse
import json
from gpiozero import LED, Buzzer
from grove.display.jhd1802 import JHD1802
from random import randint

# ID kênh Thingspeak và khóa API để đọc dữ liệu
HTTP_CHANNELID = '2650621'
Read_API_Keys = '546SD122PXP65W5M'

# Hàm để lấy dữ liệu từ Thingspeak
def thingspeak_get():
   api_key_read = Read_API_Keys
   channel_id = HTTP_CHANNELID
   data = {}
   
   # Vòng lặp qua các trường dữ liệu (field1, field2, field3) để lấy dữ liệu từ kênh Thingspeak
   for field in range(1, 4):
       # Tạo yêu cầu HTTP GET để đọc dữ liệu từ từng trường
       req = request.Request(f'https://api.thingspeak.com/channels/{channel_id}/fields/{field}/last.json?api_key={api_key_read}', method='GET')
       r = request.urlopen(req)  # Gửi yêu cầu và nhận phản hồi
       respone_data = r.read().decode()  # Đọc và giải mã dữ liệu nhận được
       respone_data = json.loads(respone_data)  # Chuyển đổi dữ liệu JSON thành dictionary
       
       # Lưu dữ liệu vào dictionary `data`, với key là field tương ứng
       data[f'field{field}'] = int(respone_data[f'field{field}'])
   return data  # Trả về dữ liệu thu thập được

# Khởi tạo các thiết bị phần cứng
bz = Buzzer(18)  # Buzzer kết nối với GPIO 18
led = LED(22)  # Đèn LED kết nối với GPIO 22
relay = LED(5)  # Relay kết nối với GPIO 5
lcd = JHD1802()  # Màn hình LCD JHD1802

# Biến để lưu trữ dữ liệu
data = {}

# Vòng lặp chính để liên tục lấy dữ liệu và điều khiển các thiết bị
while 1:
    try:
        # Lấy dữ liệu từ Thingspeak
        data = thingspeak_get()
    except Exception as e:
        print('Error download')  # In lỗi nếu xảy ra khi tải dữ liệu
        sleep(1)  # Dừng 1 giây trước khi thử lại
    
    # Điều khiển LED dựa trên giá trị của field1
    if data['field1'] > 50:
        led.on()  # Bật LED nếu giá trị field1 lớn hơn 50
    elif data['field1'] < 50:
        led.off()  # Tắt LED nếu giá trị field1 nhỏ hơn 50

    # Điều khiển Buzzer dựa trên giá trị của field2 (nhiệt độ)
    if data['field2'] > 37:
        bz.on()  # Bật Buzzer nếu nhiệt độ vượt quá 37 độ C
    elif data['field2'] < 31:
        bz.off()  # Tắt Buzzer nếu nhiệt độ dưới 31 độ C

    # Điều khiển Relay dựa trên giá trị của field3 (độ ẩm)
    if data['field3'] > 90:
        relay.on()  # Bật Relay nếu độ ẩm vượt quá 90%
    elif data['field3'] < 60:
        relay.off()  # Tắt Relay nếu độ ẩm dưới 60%

    # Cập nhật nội dung hiển thị trên màn hình LCD
    lcd.clear()  # Xóa màn hình trước khi hiển thị mới
    sleep(0.5)  # Tạm dừng 0.5 giây để đảm bảo LCD đã được xóa
    lcd.setCursor(0, 0)  # Đặt con trỏ ở dòng đầu tiên, cột đầu tiên
    lcd.write('randata: {}'.format(data['field1']))  # Hiển thị giá trị random (field1)
    lcd.setCursor(1, 0)  # Đặt con trỏ ở dòng thứ hai
    lcd.write('{}c    {}%'.format(data['field2'], data['field3']))  # Hiển thị nhiệt độ (field2) và độ ẩm (field3)
    
    sleep(20)  # Dừng 20 giây trước khi thực hiện lại vòng lặp
