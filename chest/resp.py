import time
import Adafruit_ADS1x15
from ubidots import ApiClient

adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1
time.sleep(2)
v = adc.read_adc(1, gain=GAIN)
temp =  v
maxval= v
minval= v
f=8
c=0
def addarate(mx,mn,count):
	print("difference :" + str(mx-mn))
	if mx-mn > 100:
		print("direction changed")
		count=count+1
	return count

while True:
	newval = adc.read_adc(1, gain=GAIN)
	if newval>=temp+100:
		print("Increasing bent")
        	if f==0:
			c = addarate(maxval,minval,c)
			print("count :"+ str(c) )
			f=8
		maxval=temp
		temp=newval
		f=1
	elif newval<=temp-100:
		print("Decreasing bent")
		temp = newval
		minval = temp
		f=0
#	print(val)
	time.sleep(0.02)

