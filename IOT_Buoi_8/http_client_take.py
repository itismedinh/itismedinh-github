# Nhập các thư viện cần thiết
from time import sleep
from urllib import request, parse
import json
from datetime import datetime
from random import randint
from random import uniform
from gpiozero import LED
from seeed_dht import DHT

# Tạo custom API 
API_WRITE = "nhom11-write"
API_READ = "nhom11-read"

# Cau hinh cac chan module
led1 = LED(22)
led2 = LED(24)
led3 = LED(26)
sensor = DHT("11", 5)

# Hàm upload dữ liệu thông qua http
def post_http(temp, humi, led1, led2, led3):
    data = {
        "temperature": temp,
        "humidity": humi,
        "led1": led1,
        "led2": led2,
        "led3": led3,
        "device_name": 'raspberry',
        "timestamp": datetime.now().isoformat()
    }
    params = json.dumps(data).encode()
    req = request.Request('http://192.168.1.145:8000/api', method='POST')
    req.add_header('accept', 'application/json')
    req.add_header('Content-Type', 'application/json')
    req.add_header('api_write', API_WRITE)
    response = request.urlopen(req, data = params).read()
    return response

# Hàm lấy dữ liệu thông qua http
def get_http(n=None, start_time=None, end_time=None):
    base_url = 'http://192.168.1.145:8000/api/get_data'

    query_params = {}
    
    if n is not None:
        query_params['n'] = n

    if start_time is not None and end_time is not None:
        query_params['start_time'] = parse.quote(str(start_time))
        query_params['end_time'] = parse.quote(str(end_time))

    query_str = "&".join([f"{key}={value}" for key, value in query_params.items()])
    full_url = f"{base_url}?{query_str}" if query_params else base_url

    print(f"Generated URL: {full_url}")

    try:
        req = request.Request(full_url, method='GET')
        req.add_header('accept', 'application/json')
        req.add_header('Content-Type', 'application/json')
        req.add_header('api_read', API_READ) 

        response = request.urlopen(req).read()
        array_return = json.loads(response)

        for entry in array_return:
            temperature = entry.get('temperature', None)
            humidity = entry.get('humidity', None)
            led1_status = entry.get('led1', None)
            led2_status = entry.get('led2', None)
            led3_status = entry.get('led3', None)
            timestamp = entry.get('timestamp', None)
            print(f"\nTemperature: {temperature}\nHumidity: {humidity}\nLED1: {led1_status}\nLED2: {led2_status}\nLED3: {led3_status}\nTimestamp: {timestamp}\n")

    except Exception as e:
        print(f"Error: {e}")
        return None

# Gọi hàm get_http với tham số datetime
# get_http(n=1, start_time="2024-10-12 00:06:01.778558", end_time="2024-10-12 00:17:29.009119")

while 1:
    try:
        try:
            n = int(input("n: "))
        except Exception as e:
            n = None
        start_time = input("start_time: ")
        end_time = input("end_time: ")
        if n>0 and n is not None:
            get_http(n=n)
        elif n is None and start_time is not None and end_time is not None:
            get_http(start_time=start_time, end_time=end_time)
        elif n is not None and start_time is not None and end_time is not None:
            get_http(n=n, start_time=start_time, end_time=end_time)
        
        sleep(1)
        
        humi, temp = sensor.read()
        led1_data = randint(0, 1)
        led2_data = randint(0, 1)
        led3_data = randint(0, 1)
        print(f"temp: {temp}, humi: {humi}, led1_data: {led1_data}, led2_data: {led2_data}, led3_data: {led3_data}")
        post_http(temp, humi, led1_data, led2_data, led3_data)
        if led1_data:
            led1.on()
        else:
            led1.off()
        if led2_data:
            led2.on()
        else:
            led2.off()
        if led3_data:
            led3.on()
        else:
            led3.off()
            
        sleep(5)

    except Exception as e:
        sleep(1)
        print(e)


# get_http(n=1)