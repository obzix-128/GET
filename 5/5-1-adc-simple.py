import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

dac    = [8, 11, 7, 1, 0, 5, 12, 6]
comp   = 14
troyka = 13

GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

def decimal2binary(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

def adc():
    for value in range(256):
        GPIO.output(dac, decimal2binary(value))
        time.sleep(0.001)

        if (GPIO.input(comp) == GPIO.HIGH):
            return value
    return 256

try:
    while True:
            results = adc()
            voltage = (results / 256) * 3.3

            print(f' Напряжение =  {voltage:.2f}V')

finally:
    GPIO.output(dac, GPIO.LOW)
    GPIO.output(troyka, GPIO.LOW)
    GPIO.cleanup()
