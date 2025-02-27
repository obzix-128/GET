import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

dac    = [8, 11, 7, 1, 0, 5, 12, 6]
zero   = [0, 0, 0, 0, 0, 0, 0, 0,]

GPIO.setup(dac, GPIO.OUT)

def decimal2binary(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

try:
    while (True):
        num = input("Enter intrger number from 0 to 255\n")

        try:
            num = int(num)
            if (num >= 0) and (num <= 255):
                GPIO.output(dac, decimal2binary(num))
                voltage = 3.3 * num / 256
                print ('Voltage = ',voltage)

            else:
                if (num < 0):
                    print("Num < 0")
                else: 
                    print("Num > 0")

        except Exception:
            if (num == 'q'):
                break
            print ("EXCEPT")

        except FloatingPointError:
            print("Error: Float")

finally:
    GPIO.output(dac, zero)
    GPIO.cleanup()
