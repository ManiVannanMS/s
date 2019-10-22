import max30102
import hrcalc
import numpy as np
from numpy_ringbuffer import RingBuffer
import time
from threading import Thread
from ubidots import ApiClient

api = ApiClient(token='BBFF-fL8zVhHoLgjat7rQ66WhKzi7NIZ4t4')
temperature_var = api.get_variable('5d63d2871d847219d5fe0765')
spo2_var = api.get_variable('5d63d2911d847219f03b3c03')
hr_var = api.get_variable('5d63d2831d847219f03b3bfd')
hrv_var = api.get_variable('5d63d27d1d847218bafefef5')

irb = RingBuffer(capacity = 600,dtype= np.int)
redb = RingBuffer(capacity = 600,dtype= np.int)

m = max30102.MAX30102()
print("Started Max")

def isFull():
	if len(irb)>=600:
        	return 1
        else:
        	return 0

def isEmpty():
	if len(irb)==0:
		return 1
	else:
		return 0

def producer():
	ir, red = m.read_sequential()
	irb.extend(ir)
	redb.extend(red)
	print("Produced")
	time.sleep(0.5)
	if isFull():
		#print("Buffer is Full")
		pass

def consumer():
	if isEmpty():
		print("Buffer is Empty")
	elif len(irb)>0 and len(redb)>0:
		irbl = []
		redbl = []
		hrv = -999
		for i in range(100):
			irbl.append(irb.pop())
			redbl.append(redb.pop())
		hrv,hr,hr_val,spo2,spo2_val = hrcalc.calc_hr_and_spo2(irbl, redbl)
		t = m.read_temperature()
		#print("Consumed")
		print("temperature : " + str(t))
		print(hrv,hr,hr_val,spo2,spo2_val)
		hrv = int(hrv)
		try:
			if hr_val and spo2_val:
				temperature_var.save_value({'value': t, 'context':{'Status':'Valid'}})
                        	hr_var.save_value({'value': hr, 'context':{'Status':'Valid'}})
                        	spo2_var.save_value({'value': spo2, 'context':{'Status':'Valid'}})
				hrv_var.save_value({'value': hrv, 'context':{'Status':'Valid'}})
		except:
			print('Exception')
			pass
		time.sleep(0.5)

class myClassA(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()
    def run(self):
        while True:
            producer()

class myClassB(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()
    def run(self):
        while True:
            consumer()

myClassA()
myClassB()
while True:
    pass
