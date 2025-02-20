import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.OUT)
GPIO.setup(24,GPIO.IN)

GPIO.output(23, GPIO.input(24))
