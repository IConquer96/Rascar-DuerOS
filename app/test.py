# -*- coding: utf-8 -*-

__author__ = 'Bo-Li'

#通过语音控制

#import FollowLine as follow
import wifirobots as robot
import RPi.GPIO as GPIO
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
LED_L = 11
LED_R = 8
LED_F = 7

#######################################
############管脚类型设置及初始化###########
#######################################
GPIO.setwarnings(False)

############led初始化输出模式############
GPIO.setup(LED_L,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(LED_R,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(LED_F,GPIO.OUT,initial=GPIO.LOW)


def recognize():

        command = "关闭前大灯"
        print command
        
        ############################################
        ###############命令识别######################
        ############################################
        
        if command.find(u"开") !=-1 and command.find(u"大") !=-1 and command.find(u"灯") !=-1:
                print "打开前大灯"
                robot.Open_Flight()
                if GPIO.output(LED_F) == GPIO.HIGH :
                        print "keyi"
                
        elif command.find(u"关") !=-1 and command.find(u"大") !=-1 and command.find(u"灯") !=-1:
                print "关闭前大灯"
                robot.Close_Flight
                GPIO.cleanup()
                
        elif command.find(u"前") !=-1 and command.find(u"进") !=-1:
                print "前进"
                robot.Motor_Forward()
                time.sleep(10)
                robot.Motor_Stop()
                
        elif command.find(u"后") !=-1 and command.find(u"退") !=-1:
                print "后退"
                robot.Motor_Backward()
                time.sleep(1)
                robot.Motor_Stop()
                
        elif command.find(u"左") !=-1 and command.find(u"转") !=-1:
                print "左转"
                #robot.Motor_TurnLeft()
                p = GPIO.PWM(LED_L, 3)
                p.start(20)
                time.sleep(1)
                p.stop()
                #robot.Motor_Stop()
                GPIO.output(LED_L, GPIO.LOW)
                
        elif command.find(u"右") !=-1 and command.find(u"转") !=-1:
                print "右转"
                robot.Motor_TurnRight()
                p = GPIO.PWM(LED_R, 3)
                p.start(20)
                time.sleep(0.5)
                p.stop()
                robot.Motor_Stop()
                GPIO.output(LED_R, GPIO.LOW)
        elif command.find(u"黑") !=-1 and command.find(u"线") !=-1:
                print "黑线"
                #fl()
                robot.TrackLine()
                #time.sleep(5)
                
	# 停用 PWM
	#pwm.stop()

	# 清理GPIO口
                #GPIO.cleanup()
recognize()

