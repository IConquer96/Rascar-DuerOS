import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(5,GPIO.OUT,initial=GPIO.LOW)
try:
    GPIO.output(5,GPIO.LOW)
    fun = GPIO.input(5)
    print fun
except KeyboardInterrupt:
    GPIO.cleanup()
