# Import các thư viện cần thiết
import socket
import struct
from seeed_dht import DHT
from grove.display.jhd1802 import JHD1802
from gpiozero import LED
from time import sleep
import struct

# Hàm gửi frame truyền cho master
def send_frame(UDP_Client, id_b, data, ClientAddressPort):
    start = 0x01
    end = 0xff
    lesser_frame = [start]
    lesser_frame.append(id_b)
    lesser_frame.extend(data)
    crc = sum(lesser_frame) % 256
    lesser_frame.append(crc)
    lesser_frame.append(end)
    leght = len(lesser_frame) + 1
    lesser_frame.insert(1,leght)
    
    frame = struct.pack(f'!{leght}B', *lesser_frame)
    UDP_Client.sendto(frame, ServerAddressPort)

# Hàm nhận frame truyền từ master
def recv_frame(UDP_Client):     
    message = UDP_Client.recvfrom(1024)
    start, leght, id_b = struct.unpack('!3B', message[0][:3])
    data_crc = struct.unpack(f'!{leght-3}B', message[0][3:leght])
    data = data_crc[:-2]
    crc = data_crc[-2]
    end = data_crc[-1]
    
    # Kiểm tra tính toàn vẹn dữ liệu
    valid = 1
    if start != 0x01:
        valid = 0
        print("Sai start byte!")
    if id_b != 0x01:
        valid = 0
        print("Sai id byte!")
    if leght < 8:
        valid = 0
        print("Do dai khong hop le")
    if crc != sum([start, id_b, sum(data)]) % 256:
        valid = 0
        print("CRC byte khong trung khop")
    if end != 0xff:
        valid = 0
        print("Sai stop byte")
    if valid == 1:
        return start, leght, id_b, data, crc, end
    else:
        print("Frame khong hop le!")
        sleep(1)

# Cấu hình chân cảm biến nhiệt độ độ ẩm, LCD va LED 
dht = DHT('11', 5)
lcd = JHD1802()
led1 = LED(22)
led2 = LED(24)
led3 = LED(26)
 
# Cấu hình địa chỉ UDP và độ rộng băng thông
ServerAddressPort = ("192.168.1.110", 8000)
ClientAddressPort = ("192.168.1.122", 8585)
buffersize = 1024
UDP_Client = socket.socket(family= socket.AF_INET, type= socket.SOCK_DGRAM)
UDP_Client.bind(ClientAddressPort)
UDP_Client.settimeout(5)

def main():
    # Tạo vòng lặp vô hạn để chương trình chạy liên tục
    while 1:
        try:            
            # Đọc các giá trị cảm biến và in ra LCD 
            humi, temp = dht.read()
            lcd.clear()
            sleep(0.5)
            lcd.setCursor(0, 0)
            lcd.write(f'temp: {temp}c')
            lcd.setCursor(1, 0)
            lcd.write(f'humi: {humi}%')

            # Gửi frame tryền tới master
            send_frame(UDP_Client, 0x00, [temp, humi], ServerAddressPort)

            # Nhận frame tryền từ master
            start, leght, id_b, data, crc, end = recv_frame(UDP_Client)
            print(data)
            
            # Kiểm tra frame truyền
            valid = 1
            if start != 0x01:
                valid = 0
                print("Sai start byte!")
            if id_b != 0x01:
                valid = 0
                print("Sai id byte!")
            if leght < 8:
                valid = 0
                print("Do dai khong hop le")
            if crc != sum([start, id_b, sum(data)]) % 256:
                valid = 0
                print("CRC byte khong trung khop")
            if end != 0xff:
                valid = 0
                print("Sai stop byte")

            # Nếu frame truyền hợp lệ thì điều khiển LED, không thì sẽ in ra frame không hợp lệ    
            if valid == 1:
                if data[0] == 1:
                    led1.on()
                else:
                    led1.off()
                if data[1] == 1:
                    led2.on()
                else:
                    led2.off()
                if data[2] == 1:
                    led3.on()
                else:
                    led3.off()
                sleep(1)
            else:
                print("Frame khong hop le!")
                sleep(1)
            
        except Exception as e:
            print(e)
            sleep(1)

main()