import RPi.GPIO as GPIO
from time import sleep
import time, math
import pyrebase
config = {
  "apiKey": "AIzaSyA3vAF6mX_pLlXN226xUk__3oIl--7YbCY",
  "authDomain": "iot-bike-4e692.firebaseapp.com",
  "databaseURL": "https://iot-bike-4e692.firebaseio.com/",
  "storageBucket": "iot-bike-4e692.appspot.com"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()
db.child("bike_stats").child("Distance")
db.child("bike_stats").child("RPM")
db.child("bike_stats").child("Pulse")


dist_meas = 0.00
km_per_hour = 0
rpm = 0
elapse = 0
sensor = 17
pulse = 0
start_timer = time.time()

def init_GPIO():					# initialize GPIO
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(sensor,GPIO.IN,GPIO.PUD_UP)

def calculate_elapse(channel):				# callback function
	global pulse, start_timer, elapse
	pulse+=1								# increase pulse by 1 whenever interrupt occurred
	elapse = time.time() - start_timer		# elapse for every 1 complete rotation made!
	start_timer = time.time()				# let current time equals to start_timer

def calculate_speed(r_cm):
        global pulse,elapse,rpm,dist_km,dist_meas,km_per_sec,km_per_hour
        if elapse !=0:							# to avoid DivisionByZero error
                rpm = 1/elapse * 60
                circ_cm = (2*math.pi)*r_cm			# calculate wheel circumference in CM
                dist_km = circ_cm/100000 			# convert cm to km
                km_per_sec = dist_km / elapse		# calculate KM/sec
                km_per_hour = km_per_sec * 3600		# calculate KM/h
                dist_meas = (dist_km*pulse)*1000	# measure distance traverse in meter
                return km_per_hour

        def init_interrupt():
        GPIO.add_event_detect(sensor, GPIO.FALLING, callback = calculate_elapse, bouncetime = 20)

if __name__ == '__main__':
	init_GPIO()
	init_interrupt()
	while True:
                calculate_speed(20)	# call this function with wheel radius as parameter
                #print('rpm:{0:.0f}-RPM kmh:{1:.0f}-KMH dist_meas:{2:.2f}m pulse:{3}'.format(rpm,km_per_hour,dist_meas,pulse))
                sleep(0.1)
                print('rpm:{0:.0f}-RPM'.format(rpm))
		#print('kmh:{1:.0f}-KMH'.format(km_per_hour))
		#print('dist_meas:{2:.2f}m'.format(dist_meas))
		#print('pulse:{3}'.format(pulse))
		#data = {"RPM": "Mortimer 'Morty' Smith"}
                db.child("RPM").push(rpm)
		
		


		
