import time
import board
import busio
import digitalio
from gpiozero import LED
import adafruit_lis3dh

# Hardware I2C setup. Use the CircuitPlayground built-in accelerometer if available;
# otherwise check I2C pins.
led = LED(26)
ledR = LED(19)
if hasattr(board, 'ACCELEROMETER_SCL'):
    i2c = busio.I2C(board.ACCELEROMETER_SCL, board.ACCELEROMETER_SDA)
    int1 = digitalio.DigitalInOut(board.ACCELEROMETER_INTERRUPT)
    lis3dhS = adafruit_lis3dh.LIS3DH_I2C(i2c, address=0x18, int1=int1)
    lis3dhD = adafruit_lis3dh.LIS3DH_I2C(i2c, address=0x18, int1=int1)
else:
    i2c = busio.I2C(board.SCL, board.SDA)
    int1 = digitalio.DigitalInOut(board.D9)  # Set this to the correct pin for the interrupt!
    lis3dhS = adafruit_lis3dh.LIS3DH_I2C(i2c, int1=int1)
    lis3dhD = adafruit_lis3dh.LIS3DH_I2C(i2c, int1=int1)

# Hardware SPI setup:
# spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
# cs = digitalio.DigitalInOut(board.D5)  # Set to correct CS pin!
# int1 = digitalio.DigitalInOut(board.D6)  # Set to correct pin for interrupt!
# lis3dh = adafruit_lis3dh.LIS3DH_SPI(spi, cs, int1=int1)

# Set range of accelerometer (can be RANGE_2_G, RANGE_4_G, RANGE_8_G or RANGE_16_G).
lis3dhS.range = adafruit_lis3dh.RANGE_2_G
lis3dhD.range = adafruit_lis3dh.RANGE_2_G

# Set tap detection to double taps.  The first parameter is a value:
#  - 0 = Disable tap detection.
#  - 1 = Detect single taps.
#  - 2 = Detect double taps.
# The second parameter is the threshold and a higher value means less sensiti4ve
# tap detection.  Note the threshold should be set based on the range above:
#  - 2G = 40-80 threshold
#  - 4G = 20-40 threshold
#  - 8G = 10-20 threshold
#  - 16G = 5-10 threshold

lis3dhS.set_tap(1,50)
lis3dhD.set_tap(2,20)

# Loop forever printing if a double tap is detected.
while True:
        if lis3dhS.tapped and (not lis3dhD.tapped):
            print('single Tapped!')
            led.on()
            time.sleep(1)
            led.off()
        elif lis3dhD.tapped:
            print('double Tapped!')
            ledR.on()
            time.sleep(1)
            ledR.off()
        else:
            print("no")
            time.sleep(0.01)
