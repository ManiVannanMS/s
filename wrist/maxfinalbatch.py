import max30102
import hrcalc
import numpy as np
from numpy_ringbuffer import RingBuffer
import time

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

def calculatePhase():
	print("CALCULATION PHASE")
	while not isEmpty():
		irbl = []
                redbl = []
                for i in range(100):
                        irbl.append(irb.pop())
                        redbl.append(redb.pop())
                hr,hr_val,spo2,spo2_val = hrcalc.calc_hr_and_spo2(irbl, redbl)
                print("Consumed")
                print(hr,hr_val,spo2,spo2_val)
                time.sleep(0.5)
	print("Buffer is empty")

def fetchPhase():
	print("FETCH PHASE")
	while not isFull():
        	ir, red = m.read_sequential()
        	irb.extend(ir)
        	redb.extend(red)
        	print("Produced")
        	time.sleep(0.5)
	print("Buffer is Full")

while True:
	fetchPhase()
	calculatePhase()
