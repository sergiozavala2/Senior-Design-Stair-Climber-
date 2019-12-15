import RPi.GPIO as GPIO
import time
import smbus
import math
import range
import picamera
import os
import sys
import PIL
import numpy as np
import zbarlight
#import camera
#import imu

GPIO.setmode(GPIO.BCM)

rangeS = range.range(27,24)

power_mgmt_1 = 0x6b
power_mgnt_2 = 0x6c

def get_image():
	with picamera.PiCamera() as camera:
		camera.resolution = (1024, 768)
		camera.start_preview()
		# Camera warm-up time
		time.sleep(2)
		camera.capture('foo.jpg')   

def picture():
	print ('Taking picture..')
	try:
		f = 1
		#qr_count = len(os.listdir('qr_codes'))
		get_image()
		#os.system('sudo fswebcam -d /dev/video'+sys.argv[1]+' -q qr_codes/qr_'+str(qr_count)+'.jpg')
		print ('Picture taken..')
	except Exception as e:
		f = 0
		print ('Picture couldn\'t be taken with exception ' + str(e))

	#print

	if(f):
		print ('Scanning image..')
		f = open('foo.jpg','rb')
		qr = PIL.Image.open(f);
		qr.load()

		codes = zbarlight.scan_codes('qrcode',qr)
		if(codes==None):
			#os.remove('qr_codes/qr_'+str(qr_count)+'.jpg')
			print ('No QR code found')
			return 0
		else:
			print( 'QR code(s):')
			return 1


def read_byte(reg):
	return bus.read_byte_data(address, reg)

def read_word(reg):
	h = bus.read_byte_data(address, reg)
	l = bus.read_byte_data(address, reg + 1)
	value = (h << 8) +l
	return value
def read_word_2c(reg):
	val = read_word(reg)
	if (val >= 0x8000):
		return -((65535 -val) + 1)
	else:
		return val

def dist(a,b):
	return math.sqrt((a*a) + (b*b))

def get_y_rotation(x,y,z):
	radians = math.atan2(x, dist(y,z))
	return -math.degrees(radians)

def get_x_rotation(x,y,z):
	radians = math.atan2(y, dist(x,z))
	return math.degrees(radians) 

bus = smbus.SMBus(1) # bus = smbus.SMBus(0) fuer Revision 1
address = 0x68 	     # via i2detect


bus.write_byte_data(address, power_mgmt_1, 0)


while(1):
	distance = rangeS.getRange()
	print "Distance:" , distance, "cm"
	gyro_xout = read_word_2c(0x43)
	gyro_yout = read_word_2c(0x45)
	gyro_zout = read_word_2c(0x47)
	accel_xout = read_word_2c(0x3b)
	accel_yout = read_word_2c(0x3d)
	accel_zout = read_word_2c(0x3f)

	accel_xout_scaled = accel_xout / 16384.0
	accel_yout_scaled = accel_yout / 16384.0
	accel_zout_scaled = accel_zout / 16384.0
	y =get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
	print "Y Rotation: ", y
	if(y <5):
		c = picture()
		if(c == 1):
			print("found")
		else:
			print("no find")
	else:
		print("not flat")
	time.sleep(1)