import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

zero   = [0, 0, 0, 0, 0, 0, 0, 0,]

GPIO.setup(21, GPIO.OUT)

p = GPIO.PWM(21, 50)
p.start(1)

try:
    while (True):
        inp = input ('Введите коэффициент заполнения в процентах (\'q\' для выхода):\n')
        inp = int(inp)
        if (inp == 'q'):
            p.stop()
            break
        p.start(inp)

finally:
    GPIO.cleanup()