from firebase import firebase
from time import sleep
import time, math
import RPi.GPIO as GPIO
from threading import Thread

dist_meas = 0.00
km_per_hour = 0
rpm = 0
elapse = 0
sensor = 17
servo = 18
pulse = 0
start_timer = time.time()
fanPower = 16
fanControl = 20
global res

 

firebase = firebase.FirebaseApplication('https://iot-bike-4e692.firebaseio.com/')

def init_GPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(sensor, GPIO.IN,GPIO.PUD_UP)
    GPIO.setup(servo, GPIO.OUT)
    GPIO.setup(fanPower, GPIO.OUT)
    GPIO.setup(fanControl, GPIO.OUT)
    res = GPIO.PWM(servo, 50)
    res.start(2.5)
    
    
    
def calculate_elapse(channel):
    global pulse, start_timer, elapse
    pulse += 1
    elapse = time.time() - start_timer
    start_timer = time.time()

def calculate_speed(r_cm):
    global pulse, elapse, rpm, dist_km, dist_meas, km_per_hour
    if elapse != 0:
        rpm = 1/elapse * 60
        circ_cm = (2*math.pi)*r_cm
        dist_km = circ_cm/100000
        km_per_sec = dist_km / elapse
        km_per_hour = km_per_sec * 3600
        dist_meas = (dist_km*pulse)*1000
        return km_per_hour

def init_interrupt():
    GPIO.add_event_detect(sensor, GPIO.FALLING, callback = calculate_elapse, bouncetime = 20)

init_GPIO()
init_interrupt()    
#if __name__ == '__main__':
def send_data():
    while True:
        calculate_speed(20)
        sleep(3)
        #print('rpm:{0:.0f}-RPM kmh:{1:.0f}-KMH dist_meas:{2:.2f}m pulse:{3}'.format(rpm,km_per_hour,dist_meas,pulse))
        rev = str(round(rpm))
        new_dist = (dist_meas / 1000)
        dist = str(round(new_dist, 2) )
        #new = (dist / 100)
        speed = str(round(km_per_hour))
        print('Speed: ', speed)
        print('Distance: ', dist, 'm')
        print('RPM: ', rev)
        #print('rpm:{0:.0f}-RPM'.format(rpm))
        #print('kmh:{0:.0f}-KMH'.format(km_per_hour))
        #print('distance:{0:.2f}m'.format(dist_meas))
        #print('pulse:{0}'.format(pulse))
        firebase.put('Stats', 'RPM', rev)
        firebase.put('Stats', 'Speed', speed)
        firebase.put('Stats', 'Distance', dist)
        print('-----------------------')

def get_data():

    while True:
        result = firebase.get('/Resistance', None) #Get Resistance data
        fan = firebase.get('/Fan', None) #Get Fan data
        print (result)
        print (fan)
        if(fan == "On"):
            GPIO.output(fanPower,GPIO.HIGH)
            GPIO.output(fanControl,GPIO.HIGH)
            print("Fan Power On")
        elif(fan == "Off"):
            GPIO.output(fanPower,GPIO.LOW)
            GPIO.output(fanControl,GPIO.LOW)
            print("Fan Power Off")
        else:
            print("Fan Not Working")
        if(result == "Down"):
            res = GPIO.PWM(servo, 50) # GPIO 18 for PWM with 50Hz
            res.start(3) # Initialization
            #res.ChangeDutyCycle(5)
            time.sleep(2)
            res.stop()
            print ("Resistance has gone down")
        elif(result == "Up"):
            res = GPIO.PWM(servo, 50) # GPIO 18 for PWM with 50Hz
            res.start(11.5) # Initialization
            #res.ChangeDutyCycle(7.5)
            time.sleep(2)
            res.stop()
            print("Resistance has gone up")
        else:
            res = GPIO.PWM(servo, 50) # GPIO 18 for PWM with 50Hz
            res.stop()
            sleep(1)
            print("Resistance is steady")
        sleep(3)
        
       
        
if __name__ == '__main__':
    Thread(target = send_data).start()
    Thread(target = get_data).start()



    
    



