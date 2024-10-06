from time import sleep
from urllib import request, parse
import json
from gpiozero import LED, Buzzer
from grove.display.jhd1802 import JHD1802
from random import randint

HTTP_CHANNELID = '2650621'
Read_API_Keys = '546SD122PXP65W5M'

def thingspeak_get():
   api_key_read = Read_API_Keys
   channel_id = HTTP_CHANNELID
   data = {}
   for field in range(1,4):
       req = request.Request(f'https://api.thingspeak.com/channels/{channel_id}/fields/{field}/last.json?api_key={api_key_read}',method='GET')
       r = request.urlopen(req)
       respone_data = r.read().decode()
       respone_data = json.loads(respone_data)
       
       data[f'field{field}'] = int(respone_data[f'field{field}'])
   return data
bz = Buzzer(18)
led = LED(22)
relay = LED(5)
lcd = JHD1802()
data = {}
while 1:
    try:
        data = thingspeak_get()
    except Exception as e:
        print('Error download')
        sleep(1)
    if data['field1'] > 50:
        led.on()
    elif data['field1'] < 50:
        led.off()
    if data['field2'] > 37:
        bz.on()
    elif data['field2'] < 31:
        bz.off()
    if data['field3'] > 90:
        relay.on()
    elif data['field3'] < 60:
        relay.off()
    lcd.clear()
    sleep(0.5)
    lcd.setCursor(0,0)
    lcd.write('randata: {}'.format(data['field1']))
    lcd.setCursor(1,0)
    lcd.write('Tmp:{}c humi:{}%'.format(data['field2'],data['field3']))
    sleep(20)
