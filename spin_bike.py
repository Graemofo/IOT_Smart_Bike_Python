# This is the Python code for my 4th year IOT project
# For my project, I have built my own personal spin bike trainer
# Using a Hall Effect Sensor, I can determine the speed and distance travelled
# There are 5 main functions
    # 1. init_GPIO is used to initialise all the GPIO pins with the corresponding sensors and actuators
    # 2. calculate_elapse and calculate_speed are used together to calculate the revolution of the wheel and it's speed
    # 3. send_data is used to calculate the right metrics and send the data up to Firebase
    # 4. get_data is used to listen for instructions from the Android Device, which sends data to Firebase as well
    # 5. Both send_data and get_data run on seperate threads

from firebase import firebase
from time import sleep
import time, math
import RPi.GPIO as GPIO
from threading import Thread
from subprocess import call

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

 
#Link to the Firebase real-time database
firebase = firebase.FirebaseApplication('https://iot-bike-4e692.firebaseio.com/')

#initilaise the GPIO pins
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

def send_data():
    while True:
        calculate_speed(20)
        sleep(3)
        rev = str(round(rpm))
        new_dist = (dist_meas / 1000)
        dist = str(round(new_dist, 2) )
        speed = str(round(km_per_hour))
        
        print('Speed: ', speed)
        print('Distance: ', dist, 'm')
        print('RPM: ', rev)

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
        if(fan == "On"):   #if fan string == On, turn fan on
            GPIO.output(fanPower,GPIO.HIGH)
            GPIO.output(fanControl,GPIO.HIGH)
            print("Fan Power On")
        elif(fan == "Off"): #if fan string == Off, turn fan off
            GPIO.output(fanPower,GPIO.LOW)
            GPIO.output(fanControl,GPIO.LOW)
            print("Fan Power Off")
        else:
            print("Fan Not Working")
            
        if(result == "Down"):
            exit_code = call("python3 turn_servo_right.py", shell=True)
            print ("Resistance has gone down")
        elif(result == "Up"):
            exit_code = call("python3 turn_servo_left.py", shell=True)
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



    
    



