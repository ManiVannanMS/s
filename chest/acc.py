'''
        Read Gyro and Accelerometer by Interfacing Raspberry Pi with MPU6050 using Python
'''

import smbus			#import SMBus module of I2C
from time import sleep          #import
from ubidots import ApiClient
import statistics
'''
api = ApiClient(token='BBFF-fL8zVhHoLgjat7rQ66WhKzi7NIZ4t4')
axv = api.get_variable('5d63d3d61d84721be34891fd')
ayv = api.get_variable('5d63d3e91d84721b4abdcc2c')
azv = api.get_variable('5d63d3f01d84721a64ed346d')
gxv = api.get_variable('5d63d3f41d84721bfab9ca9a')
gyv = api.get_variable('5d63d3f81d84721b080b5eee')
gzv = api.get_variable('5d63d3fd1d84721b978f200b')
mov = api.get_variable('5d660f6a1d847210ef1ac9fb')
'''
#some MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47


def MPU_Init():
	#write to sample rate register
	bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)

	#Write to power management register
	bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)

	#Write to Configuration register
	bus.write_byte_data(Device_Address, CONFIG, 0)

	#Write to Gyro configuration register
	bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)

	#Write to interrupt enable register
	bus.write_byte_data(Device_Address, INT_ENABLE, 1)

def read_raw_data(addr):
	#Accelero and Gyro value are 16-bit
        high = bus.read_byte_data(Device_Address, addr)
        low = bus.read_byte_data(Device_Address, addr+1)

        #concatenate higher and lower value
        value = ((high << 8) | low)

        #to get signed value from mpu6050
        if(value > 32768):
                value = value - 65536
        return value


bus = smbus.SMBus(1) 	# or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x68   # MPU6050 device address

MPU_Init()

print (" Reading Data from Accelerometer")

count = 0

def read_accelerometer():
	acc_x = read_raw_data(ACCEL_XOUT_H)
        acc_y = read_raw_data(ACCEL_YOUT_H)
        acc_z = read_raw_data(ACCEL_ZOUT_H)

        Ax = acc_x/2048
        Ay = acc_y/2048
        Az = acc_z/2048

	return Ax,Ay,Az

def std_dev(Ax_arr,Ay_arr,Az_arr):
	Ax_dev = statistics.stdev(Ax_arr)
	Ay_dev = statistics.stdev(Ay_arr)
	Az_dev = statistics.stdev(Az_arr)
#	print(Ax_dev, Ay_dev,Az_dev)
	net_dev = Ax_dev + Ay_dev + Az_dev
	return net_dev

while True:
#	print("Reading:",count)
	if count<100:
		if count==0:
			Ax_arr = []
			Ay_arr = []
			Az_arr = []
		Ax,Ay,Az = read_accelerometer()
 #               print ("Ax=%.2f g" %Ax, "Ay=%.2f g" %Ay, "Az=%.2f g" %Az)
                Ax_arr.append(Ax)
                Ay_arr.append(Ay)
                Az_arr.append(Az)
                count = count + 1
		sleep(0.01)
	else:
		if count==100:
		#	print (Ax_arr)
		#	print (Ay_arr)
		#	print (Az_arr)
			sd = std_dev(Ax_arr,Ay_arr,Az_arr)
			print("Standard Deviation : ", sd)
			m = (sd*100)/24
			print("Percentage movement : ", int(m))
			Ax_arr = []
			Ay_arr = []
			Az_arr = []
			count = 0
		#	mov.save_value({'value':m,'context':{'Status':'Valid'}})

	"""
	axv.save_value({'value': Ax, 'context':{'Status':'Valid'}})
	ayv.save_value({'value': Ay, 'context':{'Status':'Valid'}})
	azv.save_value({'value': Az, 'context':{'Status':'Valid'}})"""
