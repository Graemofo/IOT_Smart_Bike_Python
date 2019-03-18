import RPi.GPIO as GPIO
from time import sleep

fanPower = 16
fanControl = 20


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#GPIO.setup(sensor, GPIO.IN,GPIO.PUD_UP)
GPIO.setup(fanPower, GPIO.OUT)
GPIO.setup(fanControl, GPIO.OUT)



def test():
    GPIO.output(fanPower,GPIO.HIGH)
    GPIO.output(fanControl,GPIO.HIGH)
    print("Fan Power On")
    sleep(20)
    GPIO.output(fanPower,GPIO.LOW)
    GPIO.output(fanControl,GPIO.LOW)
    print("Fan Power Off")

test()
print("Script Runs")
