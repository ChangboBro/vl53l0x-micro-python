"""
MicroPython ST vl53l0x tof ranging sensor driver
code by ChangboBro.

initialization: tof=vl53l0x(i2c)
measure: distance=tof.measure()

This code is transplant from an Ardunio project, original code by Ted Meyers:
https://groups.google.com/d/msg/diyrovers/lc7NUZYuJOg/ICPrYNJGBgAJ
If there is any copyright problem, please contact me to delete it, sorry for that.
It's not perfect, you can't know whether it's reaching the max detection range,
and I don't know how to improve:( If you got any progress, you are welcomed to fork this project.
"""

import time
class vl53l0x:
    def __init__(self,i2c,addr=0x29):
        self.i2c=i2c
        self.addr=addr
        self.revision_id=self.read_data_at(b'\xc2')
        self.device_id=self.read_data_at(b'\xc0')
        self.ready=False
    
    def read_data_at(self,reg):
        temp=bytearray(1)
        self.i2c.writeto(self.addr,reg)
        time.sleep_ms(10)
        temp=self.i2c.readfrom(self.addr,1)
        return temp
    
    def measure(self):
        self.i2c.writeto(self.addr,b'\x00\x01')
        #time.sleep_ms(50)
        self.ready=False
        cnt=0
        val=0
        while(cnt<100):
            val=self.read_data_at(b'\x14')
            val=int.from_bytes(val,'big')
            if(val&0x01):
                self.ready=True
                break;
            else:
                time.sleep_ms(10)
                cnt+=1
        
        if(val&0x01):
            block=bytearray(11)
            block=self.i2c.readfrom(self.addr,11)
            #print("datablock %s"%block)
            distance=int.from_bytes(block[9:],'big')
            #distance=(distance%256)*256+int(distance/256)
            #distance=(distance>>8)+((distance%256)<<8)
            #print('%x'%block[len(block)-2])
            return distance
        else:
            self.ready=False
            return None
