from hcsr04 import HCSR04
import esp32
from time import sleep
from machine import Pin
import network, urequests, time, socket


esp_station = network.WLAN(network.STA_IF)
if not esp_station.isconnected():
    print('Connecting to WiFi...')
    esp_station.active(True)
    esp_station.connect('hello', '15587356')
    while not esp_station.isconnected():
        continue
print('Connected, the Network Configuration is:', esp_station.ifconfig())

# Declaring Constants:
HTTP_HEADERS = {'Content-Type': 'application/json'} 
THINGSPEAK_WRITE_API_KEY = '98LPF6R35I0I9MDY' 
UPDATE_TIME_INTERVAL = 1000  # in ms 
last_update = time.ticks_ms()

vib = Pin(5, Pin.OUT)
us = HCSR04(trigger_pin=13, echo_pin=12, echo_timeout_us=1000000)
ctr_left = Pin(4, Pin.IN)
global step_counter
step_counter=0
one_count=0.75
distance_m = 0
ctr_right = Pin(14, Pin.IN)
speed =0

'''defining a function (that sends data to thingspeak)'''
def thingspeak():
    sensors_readings = {'field1':step_counter, 'field2':distance_km,'field3':speed}
    request = urequests.post('http://api.thingspeak.com/update?api_key=' +THINGSPEAK_WRITE_API_KEY, json = sensors_readings, headers = HTTP_HEADERS )
    request.close()
    #print(sensors_readings)

while True:
    '''waking up'''
    esp32.wake_on_ext1(pins = (ctr_left,ctr_right), level = esp32.WAKEUP_ANY_HIGH)
        
    '''code for object detection'''
    distance = us.distance_cm()
    if distance <= 15:
        vib.on()
        #print(distance)
    else:
        vib.off()
        
    '''code for counting steps taken, time between steps, speed and distance covered'''
    try:
        if (ctr_left.value() == 1):
            
            '''starting time counting'''
            start = time.ticks_ms()
            
            '''calculating steps'''
            step_counter = step_counter + 1
            #print("step count is ", step_counter)
            
            '''calculating distance'''
            distance_m = step_counter*one_count
            distance_km = distance_m/1000
            #print("distance covered is ", distance_km, " km")
            
            '''calling function'''
            thingspeak()
            
            '''code for object detection'''
            while(ctr_left.value() == 1 ):
                distance = us.distance_cm()
                if distance <= 15:
                    vib.on()
                    #print(distance)
                else:
                    vib.off()
        if(ctr_right.value() == 1 ):
            
            '''time calculation'''
            end = time.ticks_ms()
            delta = time.ticks_diff(end, start)
            delta_sec = delta/1000
            
            '''speed calculation'''
            speed = (one_count/delta_sec)*(18/5)
            #print("the speed is ", speed, "km/hr")
            
            '''calculating steps'''
            step_counter = step_counter + 1
            #print("step count is ", step_counter)
            
            '''calculating distance'''
            distance_m = step_counter*one_count
            distance_km = distance_m/1000
            #print("distance covered is ", distance_km, " km")
            
            '''code for deepsleep'''
            if (delta_sec>5):
                x=5
                for time in range(5,0,-1):
                    sleep(1)
                    x=x-1
                    print(x,"sec" )
                print("IM SLEEPING")
                machine.deepsleep()
            
            '''code for object detection'''
            while(ctr_right.value() == 1 ):
                distance = us.distance_cm()
                if distance <= 15:
                    vib.on()
                    #print(distance)
                else:
                    vib.off()
    except:
        while (ctr_right.value() == 1):
            
            '''starting time counting'''
            start = time.ticks_ms()
            
            '''calculating steps'''
            step_counter = step_counter + 1
            #print("step count is ", step_counter)
            
            '''calculating distance'''
            distance_m = step_counter*one_count
            distance_km = distance_m/1000
            #print("distance covered is ", distance_km, " km")
            
            '''calling function'''
            thingspeak()
            
            '''code for object detection'''
            while(ctr_right.value() == 1 ):
                distance = us.distance_cm()
                if distance <= 15:
                    vib.on()
                    #print(distance)
                else:
                    vib.off()
            if (ctr_left.value() == 1 ):
                
                '''time calculation'''
                end = time.ticks_ms()
                delta = time.ticks_diff(end, start)
                delta_sec = delta/1000
                
                '''speed calculation'''
                speed = (one_count/delta_sec)*(18/5)
                #print("the speed is ", speed, " km/hr")
                
                '''code for deepsleep'''
                if (delta_sec>5):
                    x=5
                    for time in range(5,0,-1):
                        sleep(1)
                        x=x-1
                        print(x,"sec" )
                    print("IM SLEEPING")
                    machine.deepsleep()
                
            '''calculating steps'''
            step_counter = step_counter + 1
            #print("step count is ", step_counter)
            
            '''calculating distance'''
            distance_m = step_counter*one_count
            distance_km = distance_m/1000
            #print("distance covered is ", distance_km, " km")
            
            '''code for object detection'''
            while(ctr_left.value() == 1 ):
                distance = us.distance_cm()
                if distance <= 15:
                    vib.on()
                    #print(distance)
                else:
                    vib.off()
