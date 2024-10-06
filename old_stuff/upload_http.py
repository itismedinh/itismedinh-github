from time import sleep
from urllib import request, parse
from random import randint
from seeed_dht import DHT

HTTP_API_WRITE_KEY = '40V0WP2LK84W7H6P'

def send_http(data):
    url = 'https://api.thingspeak.com/update'
    params = parse.urlencode({
        'field1': data['rand'],
        'field2': data['temp'],
        'field3': data['humi']
    }).encode()
    req = request.Request(url, data=params, method='POST')
    req.add_header('Content-Type', 'application/x-www-form-urlencoded')
    req.add_header('X-THINGSPEAKAPIKEY', HTTP_API_WRITE_KEY)
    response = request.urlopen(req)
    return response.read()
dht = DHT('11', 26)
data = {}
while 1:
    data['rand'] = randint(0,100)
    data['humi'], data['temp'] = dht.read()
    
    if (data['humi'] is None or data['humi'] <= 0) or (data['temp'] is None or data['temp'] <= 0):
        data['humi'], data['temp'] = dht.read()
        
    try:  
        send_http(data)
    except Exception as e:
        print(f'Error Upload: {e}')
        sleep(1)
    sleep(20)
