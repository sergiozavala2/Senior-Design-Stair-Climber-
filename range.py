import RPi. GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class range(object):
	def __init__(self, TRIG1, ECHO1):
		self.TRIG = TRIG1
		self.ECHO = ECHO1
		GPIO.setup(self.TRIG,GPIO.OUT)
		GPIO.setup(self.ECHO,GPIO.IN)
		GPIO.output(self.TRIG, False)


	def getRange(self):               
		GPIO.output(self.TRIG, True)
		time.sleep(1)
		GPIO.output(self.TRIG, False)

		while GPIO.input(self.ECHO) ==0:
			pulse_start = time.time()

		while GPIO.input(self.ECHO) ==1:
			pulse_end = time.time()
		pulse_duration = pulse_end - pulse_start
		distance = pulse_duration *  17150
		distance = round(distance, 2)
		return distance