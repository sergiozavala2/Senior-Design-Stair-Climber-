#

from Adafruit_MotorHAT import Adafruit_MotorHAT

import time
import atexit

class motor_controller(object):
	def __init__(self, addr=0x60, left_f=1, right_f=2, left_b=3, right_b = 4, stop_at_exit = True): #main motors setup
		self.mh = Adafruit_MotorHAT(addr)
		self.left_front = self.mh.getMotor(left_f) #1
		self.right_front = self.mh.getMotor(right_f) #2
		self.left_front.run(Adafruit_MotorHAT.RELEASE)
		self.right_front.run(Adafruit_MotorHAT.RELEASE)
                #back motors setup
		self.left_back = self.mh.getMotor(left_b) #3
		self.right_back = self.mh.getMotor(right_b) #4
		self.left_back.run(Adafruit_MotorHAT.RELEASE)
		self.right_back.run(Adafruit_MotorHAT.RELEASE)
		if stop_at_exit:
			atexit.register(self.stop)

	def forward(self, speed = 100):
                #speed = input('Set speed: ')
                #speed = int(speed)
                #speed = max(0, min(255, speed)
		self.left_front.setSpeed(speed)
		self.left_back.setSpeed(speed)
		self.right_front.setSpeed(speed)
		self.right_back.setSpeed(speed)
		self.left_front.run(Adafruit_MotorHAT.FORWARD)
		self.left_back.run(Adafruit_MotorHAT.FORWARD)
		self.right_front.run(Adafruit_MotorHAT.FORWARD)
		self.right_back.run(Adafruit_MotorHAT.FORWARD)
		print('forward')
        
	def reverse(self, speed = 50):
		self.left_front.setSpeed(speed)
		self.right_front.setSpeed(speed)
		self.left_back.setSpeed(speed)
		self.right_back.setSpeed(speed)
		self.left_front.run(Adafruit_MotorHAT.BACKWARD)
		self.right_front.run(Adafruit_MotorHAT.BACKWARD)
		self.left_back.run(Adafruit_MotorHAT.BACKWARD)
		self.right_back.run(Adafruit_MotorHAT.BACKWARD)
		print('back')
	
	def left(self, speed = 50):
		self.left_front.setSpeed(speed)
		self.right_front.setSpeed(speed)
		self.left_back.setSpeed(speed)
		self.right_back.setSpeed(speed)
		self.left_front.run(Adafruit_MotorHAT.FORWARD)
		self.right_front.run(Adafruit_MotorHAT.BACKWARD)
		self.left_back.run(Adafruit_MotorHAT.FORWARD)
		self.right_back.run(Adafruit_MotorHAT.BACKWARD)
		print('left')
                
	def right(self, speed = 50):
		self.left_front.setSpeed(speed)
		self.right_front.setSpeed(speed)
		self.left_back.setSpeed(speed)
		self.right_back.setSpeed(speed)
		self.left_front.run(Adafruit_MotorHAT.BACKWARD)
		self.right_front.run(Adafruit_MotorHAT.FORWARD)
		self.left_back.run(Adafruit_MotorHAT.BACKWARD)
		self.right_back.run(Adafruit_MotorHAT.FORWARD)
		print('right')

	def stop(self):
		self.left_back.run(Adafruit_MotorHAT.RELEASE)
		self.right_back.run(Adafruit_MotorHAT.RELEASE)
		self.right_front.run(Adafruit_MotorHAT.RELEASE)
		self.left_front.run(Adafruit_MotorHAT.RELEASE)
		print('stop')