#!/usr/bin/python

import smbus
import math
import time

Class IMU(object):
def __init__(self, pm1 = 0x6b, pm2 = 0x6c, addr = 0x68)
self.power_mgmt_1 = pm1
self.power_mgmt_2 = pm2
self.address = addr
self.bus = smbus.SMBus(1)
bus.write_byte_data(self.address, self.power_mgmt_1, 0)

def read_byte(self, reg):
return bus.read_byte_data(self.address, reg)

def read_word(self, reg):
h = bus.read_byte_data(self.address, reg)
l = bus.read_byte_data(self.address, reg + 1)
value = (h << 8) +l
return value

def read_word_2c(self, reg):
val = read_word(reg)
if (val >= 0x8000):
return -((65535 -val) + 1)
else:
return val

def dist(self, a,b):
return math.sqrt((a*a) + (b*b))

def get_y_rotation(self, x,y,z):
radians = math.atan2(x, dist(y,z))
return -math.degrees(radians)

def get_x_rotation(self, x,y,z):
radians = math.atan2(y, dist(x,z))
return math.degrees(radians)

def Display(self):
time.sleep(1)
print "Gyroscope"

gyro_xout = read_word_2c(0x43)
gyro_yout = read_word_2c(0x45)
gyro_zout = read_word_2c(0x47)

print "Gyro_xout: ", ("%5d" % gyro_xout), "scaled: ", (gyro_xout / 131)
print "Gyro_yout: ", ("%5d" % gyro_yout), "scaled: ", (gyro_yout / 131)
print "Gyro_zout: ", ("%5d" % gyro_zout), "scaled: ", (gyro_zout / 131)

accel_xout = read_word_2c(0x3b)
accel_yout = read_word_2c(0x3d)
accel_zout = read_word_2c(0x3f)

#not sure what the scaling is about
accel_xout_scaled = accel_xout / 16384.0
accel_yout_scaled = accel_yout / 16384.0
accel_zout_scaled = accel_zout / 16384.0

print "accel_xout: " ,("%6d" % accel_xout), "scaled: ", accel_xout_scaled
print "accel_yout: " ,("%6d" % accel_yout), "scaled: ", accel_yout_scaled
print "accel_zout: " ,("%6d" % accel_zout), "scaled: ", accel_zout_scaled

print "X Rotation: " , get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
print "Y Rotation: " , get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)

time.sleep(0.000001)

def get_y_rot(self):
gyro_yout = read_word_2c(0x45)
accel_yout = read_word_2c(0x3d)
accel_yout_scaled = accel_yout / 16384.0
y = get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
return y