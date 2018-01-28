# -*- coding: utf-8 -*-

__author__ = 'Bo-Li'

#通过语音控制
#################################################################################
import wifirobots as robot
import RPi.GPIO as GPIO
import shutil
import time
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')

#######################################
#############信号引脚定义################
#######################################
GPIO.setmode(GPIO.BCM)

########LED口定义#################
LED_CTR = 5

#######################################
############管脚类型设置及初始化###########
#######################################
GPIO.setwarnings(False)

############led初始化输出模式############
GPIO.setup(LED_left,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(LED_right,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(LED_front,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(LED_CTR,GPIO.OUT,initial=GPIO.LOW)
######################################

# 识别部分

def recognize():

        file = '/home/pi/DuerOS-Python-Client/ord.txt' # 读取文件
        f = open(file,'r')
        out = f.read()
        command = out.decode('unicode-escape').encode('utf-8')
        print command
        GPIO.output(LED_CTR, GPIO.LOW)
        '''
	try:
		if command.find(u"开") !=-1 and command.find(u"大") !=-1 and command.find(u"灯") !=-1:
			print "已经为您开灯"
			GPIO.output(11, GPIO.HIGH)
		elif command.find(u"关") !=-1 and command.find(u"大") !=-1 and command.find(u"灯") !=-1:
                        print "已经为您关灯"
                        GPIO.output(11, GPIO.LOW)
	except KeyboardInterrupt:
                GPIO.cleanup()
        '''
        ############################################
        ###############命令识别######################
        ############################################
        
        if command.find(u"开") !=-1 and command.find(u"大") !=-1 and command.find(u"灯") !=-1:
                print "打开前大灯"
                robot.Open_Flight()
                GPIO.output(LED_CTR, GPIO.HIGH)
                shutil.copy("/home/pi/DuerOS-Python-Client/app/resources/turn_on_light.mp3","/home/pi/DuerOS-Python-Client/temp.mp3")
                
        elif command.find(u"关") !=-1 and command.find(u"大") !=-1 and command.find(u"灯") !=-1:
                print "关闭前大灯"
                robot.Close_Flight()
                GPIO.output(LED_CTR, GPIO.HIGH)
                shutil.copy("/home/pi/DuerOS-Python-Client/app/resources/turn_off_light.mp3","/home/pi/DuerOS-Python-Client/temp.mp3")
                
        elif command.find(u"前") !=-1 and command.find(u"进") !=-1:
                print "前进"
                robot.Motor_Forward()
                time.sleep(2)
                robot.Motor_Stop()
                GPIO.output(LED_CTR, GPIO.HIGH)
                shutil.copy("/home/pi/DuerOS-Python-Client/app/resources/forward.mp3","/home/pi/DuerOS-Python-Client/temp.mp3")
                
        elif command.find(u"后") !=-1 and command.find(u"退") !=-1:
                print "后退"
                robot.Motor_Backward()
                time.sleep(2)
                robot.Motor_Stop()
                GPIO.output(LED_CTR, GPIO.HIGH)
                shutil.copy("/home/pi/DuerOS-Python-Client/app/resources/backward.mp3","/home/pi/DuerOS-Python-Client/temp.mp3")
                
        elif command.find(u"左") !=-1 and command.find(u"转") !=-1:
                print "左转"
                robot.Motor_TurnLeft()
                p = GPIO.PWM(11, 3)
                p.start(20)
                time.sleep(0.5)
                p.stop()
                robot.Motor_Stop()
                GPIO.output(11, GPIO.LOW)
                GPIO.output(LED_CTR, GPIO.HIGH)
                shutil.copy("/home/pi/DuerOS-Python-Client/app/resources/turn_left.mp3","/home/pi/DuerOS-Python-Client/temp.mp3")
                
        elif command.find(u"右") !=-1 and command.find(u"转") !=-1:
                print "右转"
                robot.Motor_TurnRight()
                p = GPIO.PWM(8, 3)
                p.start(20)
                time.sleep(0.5)
                p.stop()
                robot.Motor_Stop()
                GPIO.output(8, GPIO.LOW)
                GPIO.output(LED_CTR, GPIO.HIGH)
                shutil.copy("/home/pi/DuerOS-Python-Client/app/resources/turn_right.mp3","/home/pi/DuerOS-Python-Client/temp.mp3")
                
        elif command.find(u"黑") !=-1 and command.find(u"线") !=-1:
                print "黑线"
                robot.TrackLine()
                
	# 停用 PWM
	#pwm.stop()

	# 清理GPIO口
                #GPIO.cleanup()
#recognize()
