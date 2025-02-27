import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

dac    = [8, 11, 7, 1, 0, 5, 12, 6]
zero   = [0, 0, 0, 0, 0, 0, 0, 0,]

GPIO.setup(dac, GPIO.OUT)

def decimal2binary(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

period = input ("Введите период в секундах: ")
period = int(period)

try:
    while (True):
        for i in range(0,255):
            GPIO.output(dac, decimal2binary(i))
            time.sleep(period/512)

        for i in range(255,0):
            GPIO.output(dac, decimal2binary(i))
            time.sleep(period/512)

finally:
    GPIO.output(dac, zero)
    GPIO.cleanup()
