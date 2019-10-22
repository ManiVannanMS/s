
import time
#from scipy.fftpack import fft
import Adafruit_ADS1x15
from numpy.fft import fftfreq,fft
#import numpy
import time
import matplotlib.pyplot as plt

#n=10000
newArr=[]
adc = Adafruit_ADS1x15.ADS1115()
l=[]
a=1

print (time.ctime())

for i in range(0,100):
    value = (adc.read_adc(1, gain=1,data_rate=8))
    l.append(value)
print (time.ctime())
f=fft(l)
#print(f)
#print("/n")
y=abs(f)
y[0]=0
print(y)
z=[]
for k in range(100):
    z.append(k)
    
plt.plot(z,y)
plt.show()
#print(len(f))
#for j in f && k in range(1000):
#   f[k]=j*860*10000

'''
while True:
    print(adc.read_adc(2, gain=GAIN))
    time.sleep(0.1)
'''
'''
while a :
    value = (adc.read_adc(2, gain=GAIN))
#    print(value)
    l.append(value)

 #   print(l)
  #  print(len(l))
    if len(l)==1000:
      a=0
      print (time.ctime())
      print(l)
#      print("\n")
      f=fft(l)
      print(f)
      print("\n")
#      print(l.size)
'''

