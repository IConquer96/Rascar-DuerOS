
# -*- coding: utf-8 -*-  
import RPi.GPIO as GPIO  
import time

#GPIO.setwarnings(False)
# BOARD编号方式，基于插座引脚编号  
GPIO.setmode(GPIO.BOARD)  
# 输出模式  
GPIO.setup(24, GPIO.OUT)
'''
try:
    #GPIO.output(23, GPIO.HIGH)  
    time.sleep(1)  
    GPIO.output(23, GPIO.LOW)  
    time.sleep(1)    
except KeyboardInterrupt:
    pass
'''
GPIO.output(24, GPIO.LOW)
GPIO.cleanup()

