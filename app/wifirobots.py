#coding:utf-8
'''
树莓派WiFi无线视频小车机器人驱动源码
作者：liuviking
版权所有：小R科技（深圳市小二极客科技有限公司）；WIFI机器人网论坛 www.wifi-robots.com
本代码可以自由修改，但禁止用作商业盈利目的！
本代码已申请软件著作权保护，如有侵权一经发现立即起诉！
'''

from socket import *
from time import ctime
import binascii
import RPi.GPIO as GPIO
import time
import threading
from smbus import SMBus


XRservo = SMBus(1)
print '....WIFIROBOTS START!!!...'


#######################################
#############信号引脚定义##############
#######################################
GPIO.setmode(GPIO.BCM)

########LED口定义#################
LED0 = 10
LED1 = 9
LED2 = 25
LED_L = 11
LED_R = 8
LED_F = 7

########电机驱动接口定义#################
ENA = 13	#//L298使能A
ENB = 20	#//L298使能B
IN1 = 19	#//电机接口1
IN2 = 16	#//电机接口2
IN3 = 21	#//电机接口3
IN4 = 26	#//电机接口4

########舵机接口定义#################

########超声波接口定义#################
ECHO = 4	#超声波接收脚位  
TRIG = 17	#超声波发射脚位

########红外传感器接口定义#################
IR_R = 18	#小车右侧巡线红外
IR_L = 27	#小车左侧巡线红外
IR_M = 22	#小车中间避障红外
IRF_R = 23	#小车跟随右侧红外
IRF_L = 24	#小车跟随左侧红外
global Cruising_Flag
Cruising_Flag = 0	#//当前循环模式
global Pre_Cruising_Flag
Pre_Cruising_Flag = 0 	#//预循环模式
buffer = ['00','00','00','00','00','00']

#######################################
#########管脚类型设置及初始化##########
#######################################
GPIO.setwarnings(False)

#########led初始化为000##########
GPIO.setup(LED0,GPIO.OUT,initial=GPIO.HIGH)
GPIO.setup(LED1,GPIO.OUT,initial=GPIO.HIGH)
GPIO.setup(LED2,GPIO.OUT,initial=GPIO.HIGH)
GPIO.setup(LED_L,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(LED_R,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(LED_F,GPIO.OUT,initial=GPIO.LOW)

#########电机初始化为LOW##########
GPIO.setup(ENA,GPIO.OUT,initial=GPIO.LOW)
ENA_pwm=GPIO.PWM(ENA,1000) 
ENA_pwm.start(0) 
ENA_pwm.ChangeDutyCycle(50)
GPIO.setup(IN1,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN2,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(ENB,GPIO.OUT,initial=GPIO.LOW)
ENB_pwm=GPIO.PWM(ENB,1000) 
ENB_pwm.start(0) 
ENB_pwm.ChangeDutyCycle(50)
GPIO.setup(IN3,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN4,GPIO.OUT,initial=GPIO.LOW)



#########红外初始化为输入，并内部拉高#########
GPIO.setup(IR_R,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(IR_L,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(IR_M,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(IRF_R,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(IRF_L,GPIO.IN,pull_up_down=GPIO.PUD_UP)



##########超声波模块管脚类型设置#########
GPIO.setup(TRIG,GPIO.OUT,initial=GPIO.LOW)#超声波模块发射端管脚设置trig
GPIO.setup(ECHO,GPIO.IN,pull_up_down=GPIO.PUD_UP)#超声波模块接收端管脚设置echo



####################################################
##函数名称 Open_Light()
##函数功能 开大灯LED_F
##入口参数 ：无
##出口参数 ：无
####################################################
def	Open_Flight():#开大灯LED_F
	GPIO.output(LED_F,GPIO.HIGH)#大灯正极接IO  负极接GND
	#time.sleep(1)

####################################################
##函数名称 Close_Light()
##函数功能 关大灯LED_F
##入口参数 ：无
##出口参数 ：无
####################################################
def	Close_Flight():#关大灯
	GPIO.output(LED_F,GPIO.LOW)#大灯正极接IO  负极接GND
	#time.sleep(1)
	
####################################################
##函数名称 init_light()
##函数功能 流水灯
##入口参数 ：无
##出口参数 ：无
####################################################
def	init_light():#流水灯
	for i in range(1, 5):
		GPIO.output(LED0,False)#流水灯LED0
		GPIO.output(LED1,False)#流水灯LED1
		GPIO.output(LED2,False)#流水灯LED2
		time.sleep(0.5)
		GPIO.output(LED0,True)#流水灯LED0
		GPIO.output(LED1,False)#流水灯LED1
		GPIO.output(LED2,False)#流水灯LED2
		time.sleep(0.5)
		GPIO.output(LED0,False)#流水灯LED0
		GPIO.output(LED1,True)#流水灯LED1
		GPIO.output(LED2,False)#流水灯LED2
		time.sleep(0.5)
		GPIO.output(LED0,False)#流水灯LED0
		GPIO.output(LED1,False)#流水灯LED1
		GPIO.output(LED2,True)#流水灯LED2
		time.sleep(0.5)
		GPIO.output(LED0,False)#流水灯LED0
		GPIO.output(LED1,False)#流水灯LED1
		GPIO.output(LED2,False)#流水灯LED2
		time.sleep(0.5)
		GPIO.output(LED0,True)#流水灯LED0
		GPIO.output(LED1,True)#流水灯LED1
		GPIO.output(LED2,True)#流水灯LED2
##########机器人方向控制###########################
def Motor_Forward():
	print 'motor forward'
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,True)
	GPIO.output(IN2,False)
	GPIO.output(IN3,True)
	GPIO.output(IN4,False)
	#time.sleep(2)
	#GPIO.output(LED1,False)#LED1亮
	#GPIO.output(LED2,False)#LED1亮
	
def Motor_Backward():
	print 'motor_backward'
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,False)
	GPIO.output(IN2,True)
	GPIO.output(IN3,False)
	GPIO.output(IN4,True)
	#time.sleep(2)
	#GPIO.output(LED1,True)#LED1灭
	#GPIO.output(LED2,False)#LED2亮
	
def Motor_TurnLeft():
	print 'motor_turnleft'
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,True)
	GPIO.output(IN2,False)
	GPIO.output(IN3,False)
	GPIO.output(IN4,True)
	#GPIO.output(LED1,False)#LED1亮
	#GPIO.output(LED2,True) #LED2灭
	
def Motor_TurnRight():
	print 'motor_turnright'
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,False)
	GPIO.output(IN2,True)
	GPIO.output(IN3,True)
	GPIO.output(IN4,False)
	#GPIO.output(LED1,False)#LED1亮
	#GPIO.output(LED2,True) #LED2灭
	
def Motor_Stop():
	print 'motor_stop'
	GPIO.output(ENA,False)
	GPIO.output(ENB,False)
	GPIO.output(IN1,False)
	GPIO.output(IN2,False)
	GPIO.output(IN3,False)
	GPIO.output(IN4,False)
	#GPIO.output(LED1,True)#LED1灭
	#GPIO.output(LED2,True)#LED2亮
	
##########机器人方向校准（模式中使用）###########################

##########机器人速度控制###########################
def ENA_Speed(EA_num):
	speed=hex(eval('0x'+EA_num))
	speed=int(speed,16)
	print 'EA_A改变啦 %d '%speed
	ENA_pwm.ChangeDutyCycle(speed)

def ENB_Speed(EB_num):
	speed=hex(eval('0x'+EB_num))
	speed=int(speed,16)
	print 'EB_B改变啦 %d '%speed
	ENB_pwm.ChangeDutyCycle(speed)	
##函数功能 ：舵机控制函数
##入口参数 ：ServoNum(舵机号)，angle_from_protocol(舵机角度)
##出口参数 ：无
####################################################
def Angle_cal(angle_from_protocol):
	angle=hex(eval('0x'+angle_from_protocol))
	angle=int(angle,16)
	if angle > 160:
		angle=160
	elif angle < 15:
		angle=15
	return angle
	
def SetServoAngle(ServoNum,angle_from_protocol):
	GPIO.output(LED0,False)
	GPIO.output(LED1,True)
	GPIO.output(LED2,False)
	time.sleep(0.01)
	GPIO.output(LED0,True)
	GPIO.output(LED1,True)
	GPIO.output(LED2,True)
	if ServoNum== 1:
		XRservo.XiaoRGEEK_SetServo(0x01,Angle_cal(angle_from_protocol))
		return
	elif ServoNum== 2:
		XRservo.XiaoRGEEK_SetServo(0x02,Angle_cal(angle_from_protocol))
		return
	elif ServoNum== 3:
		XRservo.XiaoRGEEK_SetServo(0x03,Angle_cal(angle_from_protocol))
		return
	elif ServoNum== 4:
		XRservo.XiaoRGEEK_SetServo(0x04,Angle_cal(angle_from_protocol))
		return
	elif ServoNum== 5:
		XRservo.XiaoRGEEK_SetServo(0x05,Angle_cal(angle_from_protocol))
		return
	elif ServoNum== 6:
		XRservo.XiaoRGEEK_SetServo(0x06,Angle_cal(angle_from_protocol))
		return
	elif ServoNum== 7:
		XRservo.XiaoRGEEK_SetServo(0x07,Angle_cal(angle_from_protocol))
		return
	elif ServoNum== 8:
		XRservo.XiaoRGEEK_SetServo(0x08,Angle_cal(angle_from_protocol))
		return
	else:
		return




####################################################
##函数名称 ：Avoiding()
##函数功能 ：红外避障函数
##入口参数 ：无
##出口参数 ：无
####################################################
def	Avoiding(): #红外避障函数
	if GPIO.input(IR_M) == False:
		Motor_Stop()
		time.sleep(0.1)
		return

####################################################
##函数名称 TrackLine()
##函数功能 巡黑线模式
##入口参数 ：无
##出口参数 ：无
####################################################
def TrackLine():
	if (GPIO.input(IR_L) == False)&(GPIO.input(IR_R) == False): #黑线为高，地面为低
		Motor_Forward()
		return
	elif (GPIO.input(IR_L) == False)&(GPIO.input(IR_R) == True):
		Motor_TurnRight()
		return
	elif (GPIO.input(IR_L) == True)&(GPIO.input(IR_R) == False):
		Motor_TurnLeft()
		return
	elif (GPIO.input(IR_L) == True)&(GPIO.input(IR_R) == True): #两侧都碰到黑线
		Motor_Stop()
		return

####################################################
##函数名称 Follow()
##函数功能 跟随模式
##入口参数 ：无
##出口参数 ：无
####################################################
def Follow(): 
	if(GPIO.input(IR_M) == True): #中间传感器OK
		if(GPIO.input(IRF_L) == False)&(GPIO.input(IRF_R) == False):	#俩边同时探测到障碍物
			Motor_Stop()			#停止 
		if(GPIO.input(IRF_L) == False)&(GPIO.input(IRF_R) == True):		#左侧障碍物
			Motor_TurnRight()		#右转 
		if(GPIO.input(IRF_L) == True)& (GPIO.input(IRF_R) == False):		#右侧障碍物
			Motor_TurnLeft()		#左转
		if(GPIO.input(IRF_L) == True)& (GPIO.input(IRF_R) == True):		#无任何障碍物
			Motor_Forward()			#直行 
	else:
		Motor_Stop()


####################################################
##函数名称 ：Get_Distence()
##函数功能 超声波测距，返回距离（单位是厘米）
##入口参数 ：无
##出口参数 ：无
####################################################
def	Get_Distence():
	time.sleep(0.1)
	GPIO.output(TRIG,GPIO.HIGH)
	time.sleep(0.000015)
	GPIO.output(TRIG,GPIO.LOW)
	while not GPIO.input(ECHO):
				pass
	t1 = time.time()
	while GPIO.input(ECHO):
				pass
	t2 = time.time()
	time.sleep(0.1)
	return (t2-t1)*340/2*100

####################################################
##函数名称 AvoidByRadar()
##函数功能 超声波避障函数
##入口参数 ：无
##出口参数 ：无
####################################################
def	AvoidByRadar(distance):
	dis = int(Get_Distence())
	if(distance<10):
		distance = 10					#限定最小避障距离为10cm
	if((dis>1)&(dis < distance)):		#避障距离值(单位cm)，大于1是为了避免超声波的盲区
		Motor_Stop()
	
		
def	Avoid_wave():
	dis = Get_Distence()
	if dis<15:
		Motor_Stop()
	else:
		Motor_Forward()


####################################################
##函数名称 Send_Distance()
##函数功能 ：超声波距离PC端显示
##入口参数 ：无
##出口参数 ：无
####################################################
def	Send_Distance():
	dis_send = int(Get_Distence())
	#dis_send = str("%.2f"%dis_send)
	if dis_send < 255:
		print 'Distance: %d cm' %dis_send
		tcpCliSock.send("\xFF")
		time.sleep(0.005)
		tcpCliSock.send("\x03")
		time.sleep(0.005)
		tcpCliSock.send("\x00")
		time.sleep(0.005)
		tcpCliSock.send(chr(dis_send))
		time.sleep(0.005)
		tcpCliSock.send("\xFF")
		time.sleep(0.1)


####################################################
##函数名称 Cruising_Mod()
##函数功能 ：模式切换函数
##入口参数 ：无
##出口参数 ：无
####################################################
def	Cruising_Mod(func):
	print 'into Cruising_Mod-01'
	global Pre_Cruising_Flag
	print 'Pre_Cruising_Flag %d '%Pre_Cruising_Flag
	
	global Cruising_Flag
	print 'Cruising_Flag %d '%Cruising_Flag
	while True:
		if (Pre_Cruising_Flag != Cruising_Flag):			
			if (Pre_Cruising_Flag != 0):
				Motor_Stop()
			Pre_Cruising_Flag = Cruising_Flag
			print 'Pre_Cruising_Flag = Cruising_Flag == 0'
		if(Cruising_Flag == 1):		#进入红外跟随模式
			Follow()
		elif (Cruising_Flag == 2):	#进入红外巡线模式
			TrackLine()
		elif (Cruising_Flag == 3):	#进入红外避障模式
			Avoiding()
		elif (Cruising_Flag == 4):	#进入超声波壁障模式##
			Avoid_wave()
		elif (Cruising_Flag == 5):	#进入超声波测距模式
			Send_Distance()
		elif (Cruising_Flag == 6):	#进入超声波壁障模式
			AvoidByRadar(15)
		else:
			time.sleep(0.001)
		time.sleep(0.001)
####################################################
##函数名称 Communication_Decode()
##函数功能 ：通信协议解码
##入口参数 ：无
##出口参数 ：无
####################################################    
def Communication_Decode():
	global Pre_Cruising_Flag
	global Cruising_Flag
	print 'Communication_decoding...'
	if buffer[0]=='00':
		if buffer[1]=='01':				#前进
			Motor_Forward()
		elif buffer[1]=='02':			#后退
			Motor_Backward()
		elif buffer[1]=='03':			#左转
			Motor_TurnLeft()
		elif buffer[1]=='04':			#右转
			Motor_TurnRight()
		elif buffer[1]=='00':			#停止
			Motor_Stop()
		else:
			Motor_Stop()
	elif buffer[0]=='02':
		if buffer[1]=='01':#左速度
			ENA_Speed(buffer[2])
		elif buffer[1]=='02':#右侧速度
			ENB_Speed(buffer[2])			
	elif buffer[0]=='01':
		if buffer[1]=='01':#1号舵机驱动
			SetServoAngle(1,buffer[2])
		elif buffer[1]=='02':#2号舵机驱动
			SetServoAngle(2,buffer[2])
		elif buffer[1]=='03':#3号舵机驱动
			SetServoAngle(3,buffer[2])
		elif buffer[1]=='04':#4号舵机驱动
			SetServoAngle(4,buffer[2])
		elif buffer[1]=='05':#5号舵机驱动
			SetServoAngle(5,buffer[2])
		elif buffer[1]=='06':#6号舵机驱动
			SetServoAngle(6,buffer[2])
		elif buffer[1]=='07':#7号舵机驱动
			SetServoAngle(7,buffer[2])
		elif buffer[1]=='08':#8号舵机驱动
			SetServoAngle(8,buffer[2])
		else:
			print '舵机角度大于170'
	elif buffer[0]=='13':
		if buffer[1]=='01':
			Cruising_Flag = 1#进入红外跟随模式
			print 'Cruising_Flag红外跟随模式 %d '%Cruising_Flag
		elif buffer[1]=='02':#进入红外巡线模式
			Cruising_Flag = 2
			print 'Cruising_Flag红外巡线模式 %d '%Cruising_Flag
		elif buffer[1]=='03':#进入红外避障模式
			Cruising_Flag = 3
			print 'Cruising_Flag红外避障模式 %d '%Cruising_Flag
		elif buffer[1]=='04':#进入超声波壁障模式
			Cruising_Flag = 4
			print 'Cruising_Flag超声波壁障 %d '%Cruising_Flag
		elif buffer[1]=='05':#进入超声波距离PC显示
			Cruising_Flag = 5
			print 'Cruising_Flag超声波距离PC显示 %d '%Cruising_Flag
		elif buffer[1]=='06':
			Cruising_Flag = 6
			print 'Cruising_Flag超声波遥控壁障 %d '%Cruising_Flag
		elif buffer[1]=='00':
			Cruising_Flag = 0
			print 'Cruising_Flag正常模式 %d '%Cruising_Flag
		#else:
			#Cruising_Flag = 0
	elif buffer[0]=='32':		#存储角度
		XRservo.XiaoRGEEK_SaveServo()
	elif buffer[0]=='33':		#读取角度
		XRservo.XiaoRGEEK_ReSetServo()
	elif buffer[0]=='04':		#开关灯模式 FF040000FF开灯  FF040100FF关灯
		if buffer[1]=='00':
			Open_Light()
		elif buffer[1]=='01':
			Close_Light()
		else:
			print 'error1 command!'
	elif buffer[0]=='05':		#读取电压 FF050000FF
		if buffer[1]=='00':
			Vol = XRservo.XiaoRGEEK_ReadVol()
			print 'Read_Voltage %d '%Vol
		else:
			print 'error2 command!'
	elif buffer[0]=='06':		#读取脉冲 FF060000FF读取脉冲1号  FF060100FF读取脉冲2号
		if buffer[1]=='00':
			Speed1 = XRservo.XiaoRGEEK_SpeedCounter1()
			print 'Read_Voltage %d '%Speed1
		elif buffer[1]=='01':
			Speed2 = XRservo.XiaoRGEEK_SpeedCounter2()
			print 'Read_Voltage %d '%Speed2
		else:
			print 'error3 command!'
	else:
		print 'error4 command!'


'''

init_light()

#定义TCP服务器相关变量
HOST=''
PORT=2001
BUFSIZ=1
ADDR=(HOST,PORT)
rec_flag=0
i=0
buffer=[]
#启动TCP服务器，监听2001端口
tcpSerSock=socket(AF_INET,SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(1)

threads = []
t1 = threading.Thread(target=Cruising_Mod,args=(u'监听',))
threads.append(t1)

for t in threads:
		t.setDaemon(True)
		t.start()

while True:
    print 'waitting for connection...'
    tcpCliSock,addr=tcpSerSock.accept()
    print '...connected from:',addr
    while True:
        try:
            data=tcpCliSock.recv(BUFSIZ)
            data=binascii.b2a_hex(data)
        except:
            print "Error receiving:"
            break
        
        if not data:
            break
        if rec_flag==0:
            if data=='ff':  
                buffer[:]=[]
                rec_flag=1
                i=0
        else:
            if data=='ff':
                rec_flag=0
                if i==3:
                    print 'Got data',str(buffer)[1:len(str(buffer)) - 1],"\r"
                    Communication_Decode();
                i=0
            else:
                buffer.append(data)
                i+=1
   
        #print(binascii.b2a_hex(data))
    tcpCliSock.close()
tcpSerSock.close()
'''

