import time
import Adafruit_ADS1x15
from ubidots import ApiClient

api = ApiClient(token='BBFF-fL8zVhHoLgjat7rQ66WhKzi7NIZ4t4')
gsr_var = api.get_variable('5d63d2961d847219d5fe076c')

adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1
while True:
    value = adc.read_adc(1, gain=GAIN)
    print(value)
    gsr_var.save_value({'value': value})
    time.sleep(0.5)
