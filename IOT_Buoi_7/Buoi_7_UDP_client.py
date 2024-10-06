import socket
import struct
from seeed_dht import DHT
from grove.display.jhd1802 import JHD1802
from gpiozero import LED
from time import sleep
import struct

def send_frame(UDP_Client, id_b, data, ClientAddressPort):
    # Cau hinh start byte 1, end 255
    start = 0x01
    end = 0xff
    
    # Them start byte vao frame
    lesser_frame = [start]
    lesser_frame.append(id_b)
    
    # Them cac data byte vao frame
    lesser_frame.extend(data)
    
    # Tinh crc cua frame va them vao frame
    crc = sum(lesser_frame) % 256
    lesser_frame.append(crc)
    
    # Them end byte vao frame
    lesser_frame.append(end)
    
    # Tinh do dai frame va them vao truoc data byte
    leght = len(lesser_frame) + 1
    lesser_frame.insert(1,leght)
    
    # Dong goi frame va gui qua Master
    frame = struct.pack(f'!{leght}B', *lesser_frame)
    UDP_Client.sendto(frame, ServerAddressPort)

def recv_frame(UDP_Client):
    # Nhan va unpack frame
    message = UDP_Client.recvfrom(1024)
    start, leght, id_b = struct.unpack('!3B', message[0][:3])
    data_crc = struct.unpack(f'!{leght-3}B', message[0][3:leght])
    data = data_crc[:-2]
    crc = data_crc[-2]
    end = data_crc[-1]
    
    # Kiem tra toan ven du lieu
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

# Cau hinh chan cam bien, LCD va LED 
dht = DHT('11', 5)
lcd = JHD1802()
led1 = LED(22)
led2 = LED(24)
led3 = LED(26)

# Cau hinh dia chi UDP va do rong bang thong
ServerAddressPort = ("192.168.1.110", 8000)
ClientAddressPort = ("192.168.1.122", 8585)
buffersize = 1024
UDP_Client = socket.socket(family= socket.AF_INET, type= socket.SOCK_DGRAM)
UDP_Client.bind(ClientAddressPort)
UDP_Client.settimeout(5)

def main():
    while 1:
        try:
            # Bat dau thu ket noi voi UDP
            humi, temp = dht.read()
            lcd.clear()
            sleep(0.5)
            lcd.setCursor(0, 0)
            lcd.write(f'temp: {temp}c')
            lcd.setCursor(1, 0)
            lcd.write(f'humi: {humi}%')

            send_frame(UDP_Client, 0x00, [temp, humi], ServerAddressPort)
            start, leght, id_b, data, crc, end = recv_frame(UDP_Client)
            print(data)
            
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
        except Exception as e:
            print(e)
            sleep(1)

main()