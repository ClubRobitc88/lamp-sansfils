import network
import urequests
import ujson
import utime
from machine import Pin
import ntptime
import gc
gc.collect()
ssid = 'post1'
password = '12345678'
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)
while station.isconnected() == False:
    pass
print('connexion établie')
ntptime.settime()
time_offset = 946684800
led = Pin(2, Pin.OUT)
while True:
    res = urequests.get('https://lamp-3a248-default-rtdb.europe-west1.firebasedatabase.app' + '/lamp.json')
    res = res.json()
    led_status = res["etat"]
    
    try:
        temps = res['temps']
    except:
        temps = []
    curr_time = (utime.time() + time_offset) * 1000
    print(curr_time)
    print(temps)
    for i in range(len(temps)):
        if curr_time == temps[i]["debut"]:
            print("DEBUT")
            res["etat"] = True
            urequests.put('https://lamp-3a248-default-rtdb.europe-west1.firebasedatabase.app' + '/lamp.json', data=ujson.dumps(res))
            break
        if curr_time == temps[i]["fin"]:
            print("FIN")
            res["etat"] = False
            urequests.put('https://lamp-3a248-default-rtdb.europe-west1.firebasedatabase.app' + '/lamp.json', data=ujson.dumps(res))
            break
    del temps
    gc.collect()

        
    if led_status == True:
        print('LED ON')
        led.value(1)
    if led_status == False:
        print('LED OFF')
        led.value(0)
    
    print(gc.mem_free())

