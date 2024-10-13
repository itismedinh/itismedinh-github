# Import các thư viện cần thiết
import socket
from time import sleep
import requests
import struct
from random import randint

# Khai báo kênh và API write key của ThinkSpeak
CHANNEL_ID = '2681652'
API_WRITE = 'UBMNQDNC320I3TJA'

# Hàm gửi dữ liệu lên server ThinkSpeak thông qua http
def send_http(tb_temp, tb_humi):
    url = f"https://api.thingspeak.com/update?api_key={API_WRITE}&field1={tb_temp}&field2={tb_humi}"
    requests.post(url)

# Hàm gửi frame truyền cho slave
def send_frame(UDP_Server, id_b, data, ClientAddressPort):
#   Dinh dang frame: start leght id_b data crc end
    start = 0x01
    end = 0xFF
    lesser_frame = [start]
    lesser_frame.append(id_b)
    lesser_frame.extend(data)
    crc = sum(lesser_frame) % 256
    lesser_frame.append(crc)
    lesser_frame.append(end)
    leght = len(lesser_frame) + 1
    lesser_frame.insert(1,leght)
    frame = struct.pack(f'!{leght}B', *lesser_frame)
    UDP_Server.sendto(frame, ClientAddressPort)

# Hàm nhận frame truyền từ slave
def recv_frame():
    #start byte thiet lap
    message = UDP_Server.recvfrom(1024)
    start, leght, id_b = struct.unpack('!3B', message[0][:3])
    data_crc = struct.unpack(f'!{leght-3}B', message[0][3:leght])
    data = data_crc[:-2]
    crc = data_crc[-2]
    end = data_crc[-1]
    return start, leght, id_b, data, crc, end

# Cấu hình địa chỉ UDP và độ rộng băng thông
LocaLIP = "192.168.1.110"
LocalPort = 8000
buffersize = 1024
ClientAddressPort = ("192.168.1.122",8585)
UDP_Server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDP_Server.settimeout(5)
UDP_Server.bind((LocaLIP, LocalPort))
print("UDP server up and Listening")

# Tạo dictinary cho data nhiệt độ độ ẩm và biến đếm 
data = {
    'temp':None,
    'humi':None
}
tb_temp, tb_humi = 0, 0
solandem = 0

# Tạo vòng lặp vô hạn để chương trình chạy liên tục
while (1):
    try:
        # Nhận frame tryền từ slave
        start, leght, id_b, data, crc, end = recv_frame()

        # Kiểm tra tính toàn vẹn
        valid = 1
        if start != 1:
            valid = 0
            print("Sai start byte!")
        if id_b != 0x00:
            valid = 0
            print("Sai id byte!")
        if leght < 7:
            valid = 0
            print("Sai kich thuoc")
        if crc != sum([start,id_b,sum(data)]) % 256:
            valid = 0
            print("CRC byte khong trung khop")
        if end != 0xff:
            valid = 0
            print("Sai stop byte!")

        # Nếu dữ liệu toàn vẹn sẽ tính nhiệt độ trung bình và gửi cho slave 
        if valid == 1:
            solandem += 1
            tb_temp += data[0]
            tb_humi += data[1]

            # Tạo giá trị LED ngẫu nhiên để điều khiển
            led = [0 ,0 ,0]
            for i in range(0,3):
                led[i] = randint(0,1)
            send_frame(UDP_Server, 0x01, led, ClientAddressPort)
            print (f"{solandem} Message from Client: {data[0]}c {data[1]}%")
            if solandem >= 20:
                tb_temp /= 20
                tb_humi /= 20
                send_http(tb_temp, tb_humi)
                tb_temp, tb_humi = 0, 0
                solandem = 0
                tb_temp, tb_humi = 0, 0
        else:
            print("Frame khong hop le!")
            sleep(1)
    except Exception as e:
        print(e)
        sleep(1)
