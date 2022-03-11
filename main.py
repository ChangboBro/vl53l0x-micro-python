from machine import Pin,I2C
import time
from vl53l0x import vl53l0x

i2c=I2C(0,scl=Pin(1),sda=Pin(0),freq=200000)
tof=vl53l0x(i2c)
time.sleep_ms(100)
while(1):
    distance=tof.measure()
    time.sleep_ms(100)
    if(tof.ready):
        #print("ready")
        print("distance: %d"%distance)
    else:
        print("not ready")