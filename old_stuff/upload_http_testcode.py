# Lấy các thư viện cần thiết
from time import sleep
from urllib import request, parse
from random import randint
from seeed_dht import DHT

# Khóa API để gửi dữ liệu lên Thingspeak
HTTP_API_WRITE_KEY = '40V0WP2LK84W7H6P'

# Hàm để gửi dữ liệu lên Thingspeak qua HTTP POST
def send_http(data):
    url = 'https://api.thingspeak.com/update'  # Địa chỉ URL của Thingspeak
    # Mã hóa các tham số gửi đi, bao gồm giá trị random, nhiệt độ và độ ẩm
    params = parse.urlencode({
        'field1': data['rand'],  # Giá trị random
        'field2': data['temp'],  # Nhiệt độ
        'field3': data['humi']   # Độ ẩm
    }).encode()
    # Tạo một request HTTP POST với các tham số đã mã hóa
    req = request.Request(url, data=params, method='POST')
    # Thêm header cho request để thông báo kiểu dữ liệu gửi đi là x-www-form-urlencoded
    req.add_header('Content-Type', 'application/x-www-form-urlencoded')
    # Thêm header chứa API Key của Thingspeak
    req.add_header('X-THINGSPEAKAPIKEY', HTTP_API_WRITE_KEY)
    # Gửi request và nhận phản hồi từ server
    response = request.urlopen(req)
    return response.read()

# Khởi tạo cảm biến DHT với loại DHT11 và kết nối tại GPIO 26
dht = DHT('11', 26)

# Biến để lưu trữ dữ liệu
data = {}

# Vòng lặp chính, chạy liên tục để thu thập và gửi dữ liệu
while 1:
    # Thu thập dữ liệu từ cảm biến và tạo giá trị ngẫu nhiên
    while 1:
        data['rand'] = randint(0,100)  # Tạo giá trị ngẫu nhiên từ 0 đến 100
        # Đọc độ ẩm và nhiệt độ từ cảm biến DHT
        data['humi'], data['temp'] = dht.read()
        # Nếu dữ liệu hợp lệ (không phải None), thoát khỏi vòng lặp con
        if data['rand'] is not None and data['humi'] is not None and data['temp'] is not None:
            break
        else:
            # Nếu dữ liệu không hợp lệ, tiếp tục đọc lại
            continue
    try:  
        # Gửi dữ liệu lên Thingspeak
        send_http(data)
    except Exception as e:
        # Xử lý lỗi nếu có vấn đề khi gửi dữ liệu
        print(f'Error Upload: {e}')
        sleep(1)  # Tạm dừng 1 giây nếu lỗi xảy ra
    sleep(20)  # Đợi 20 giây trước khi thu thập và gửi dữ liệu lần tiếp theo
