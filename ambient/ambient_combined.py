import time
import board
from busio import I2C
import adafruit_bme680
import busio
import adafruit_tsl2591

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_tsl2591.TSL2591(i2c)

i2c = I2C(board.SCL, board.SDA)
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False)
bme680.sea_level_pressure = 1013.25

while True:
    print('Total light: {0}lux'.format(sensor.lux))
    print('Infrared light: {0}'.format(sensor.infrared))
    print('Visible light: {0}'.format(sensor.visible))
    print('Full spectrum (IR + visible) light: {0}'.format(sensor.full_spectrum))
    #print("core_Temp = %" % vcgencmd measure_temp)
    print("\nTemperature: %0.1f C" % bme680.temperature)
    print("Gas: %d ohm" % bme680.gas)
    print("Humidity: %0.1f %%" % bme680.humidity)
    print("Pressure: %0.3f hPa" % bme680.pressure)
    print("Altitude = %0.2f meters" % bme680.altitude)
    print("*****************************************************************")
    time.sleep(1.0)
