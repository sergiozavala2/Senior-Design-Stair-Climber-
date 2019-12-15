import RPi.GPIO as GPIO
import time
import smbus
import math
import m_test
import range
import picamera
import zbarlight
import os
import sys
import PIL
import numpy as np
import lock
from Tkinter import *

#GPIO.setmode(GPIO.BCM)
#GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#def interrupt_handler():
#        print("interrupt has been pressed. Now exiting")
#        exit()

#GPIO.add_event_detect(17, GPIO.RISING, callback=interrupt_handler)
 
motorControl = m_test.m_test()
rangeS = range.range(27,24)


power_mgmt_1 = 0x6b
power_mgnt_2 = 0x6c

pin_1 = 17
#GPIO.setup(pin_1, GPIO.OUT)
#p = GPIO.PWM(pin_1, 50)

mSpeed = 200


def get_image():
	with picamera.PiCamera() as camera:
		camera.resolution = (1024, 768)
		camera.start_preview()
		# Camera warm-up time
		#time.sleep(2)
		camera.capture('foo.jpg')   

def picture():
	#print ('Taking picture..')
	try:
		f = 1
		#qr_count = len(os.listdir('qr_codes'))
		get_image()
		#os.system('sudo fswebcam -d /dev/video'+sys.argv[1]+' -q qr_codes/qr_'+str(qr_count)+'.jpg')
		#print ('Picture taken..')
	except Exception as e:
		f = 0
		print ('Picture couldn\'t be taken with exception ' + str(e))

	#print

	if(f):
		#print ('Scanning image..')
		f = open('foo.jpg','rb')
		qr = PIL.Image.open(f);
		qr.load()

		codes = zbarlight.scan_codes('qrcode',qr)
		if(codes==None):
			#os.remove('qr_codes/qr_'+str(qr_count)+'.jpg')
			#print ('No QR code found')
			return 0
		else:
			#print( 'QR code(s):',codes)
			c = convert(codes)
			return c

def convert(list):
	s = [str(i) for i in list]
	res = int("".join(s))
	return(res)


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
address = 0x68       # via i2detect


bus.write_byte_data(address, power_mgmt_1, 0)

floorS = 2
current_floor = 2

window = Tk()
 
window.title("Test env")
 
window.geometry('350x200')
 
lbl = Label(window, text="test")
 
lbl.grid(column=0, row=0)
 
def floor1():
	global floorS
	floorS = 1
	print "look for floor 1"
	search()

def floor2():
	global floorS
	floorS = 2
	print "look for floor 2"
	search()

def floor3():
	global floorS
	floorS = 3
	print "look for floor 3"
	search()

def search():
	if(current_floor == floorS):
		motorControl.stop()
		print "currently on this floor"
	elif(current_floor < floorS):
		print "need to go up"
		motorControl.right(speed = mSpeed)
		time.sleep(7)
		window.update()
		motorControl.reverse(speed = mSpeed)
		window.after(2000, g_range)
	elif(current_floor > floorS):
		print "need to go down"
		motorControl.right(speed = mSpeed)
		time.sleep(15)
		window.update()
		motorControl.reverse(speed = mSpeed)
		window.after(2000, g_range)
	else:
		print "I'm lost. Stopping for mommy"
		motorControl.stop()


def lock():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(pin_1, GPIO.OUT)
	p = GPIO.PWM(pin_1, 50)
	p.start(0)
	p.ChangeDutyCycle(12.5)
	time.sleep(0.1)
	window.update()
	p.stop()
	print("closing")
	#GPIO.cleanup()

def unlock():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(pin_1, GPIO.OUT)
	p = GPIO.PWM(pin_1, 50)
	p.start(0)
	p.ChangeDutyCycle(2.5)
	time.sleep(0.1)
	window.update()
	p.stop()
	print("opening")
	#GPIO.cleanup()


def g_range():
	global current_floor
	#distance = rangeS.getRange()
	#print "Distance:" , distance, "cm"
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
        #print "Y Rotation: ", y
	if y < 5 and y > -5:
		#print "on flat ground"
		c = picture()
		window.update()
		print"c = ", c
		print"floorS = ", floorS
		if(c == 2 or c ==1 or c ==3):
			current_floor = c
		print"current = ", current_floor
		if(c == floorS):
			motorControl.stop()
			print("floor found")
		else:
			print("wrong floor")
			window.after(2000, g_range)
		#if distance < 10:
			#motorControl.stop()
			#print "stopping. close to object"
	#window.after(2000, g_range)
 
floor1 = Button(window, text="floor1", command=floor1) 
floor1.grid(column=1, row=0)

floor2 = Button(window, text="floor2", command=floor2)
floor2.grid(column=1, row=1)

floor3 = Button(window, text="floor3", command=floor3)
floor3.grid(column=1, row=2)

unlock = Button(window, text="open", command=unlock)
unlock.grid(column=2, row=1)

lock = Button(window, text="close", command=lock)
lock.grid(column=2, row =2)

#right = Button(window, test ="right", command=right)
#right.grid(column=3, row=0)

#left = Button(window, test ="left", command = left)
#left.grid(column=3, row=2)

window.after(2000, g_range)

window.mainloop()