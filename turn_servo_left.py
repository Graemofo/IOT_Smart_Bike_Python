import RPi.GPIO as GPIO
import time

servoPIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) # GPIO 18 for PWM with 50Hz
p.start(2.5) # Initialization

#one rotation anti-clockwise.
p.ChangeDutyCycle(7.5)
time.sleep(2)
#stop servo and cleanup pins
p.stop()
GPIO.cleanup()
