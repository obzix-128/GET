import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
import time

def dec2bin(value):
    return [int(i) for i in bin(value)[2:].zfill(8)]

def bin2dec(value):
    string = ''
    for i in value:
        string += str(i)
    return int(string, base = 2)

def adc(dac):
    level = [0] * 8
    for i in range(8):
        level[i] = 1
        GPIO.output(dac, level)
        time.sleep(0.01)
        comp_value = GPIO.input(comp)
        if comp_value == 1:
            level[i] = 0
        GPIO.output(dac, level)
    return bin2dec(level)

dac = [6, 11, 7, 1, 0, 5, 12, 6]
leds = [2, 3, 4, 17, 27, 22, 10, 9]
comp = 14
tryoka = 13
levels = 256
maxV = 3.3

GPIO.setmode(GPIO.BCM)

GPIO.setup(tryoka, GPIO.OUT)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(comp, GPIO.IN)
GPIO.setup(leds, GPIO.OUT, initial = GPIO.LOW)

voltage_data = []
time_data = []

try:
    start = time.time()
    GPIO.output(tryoka, GPIO.HIGH)
    val = 0
    while val < 200:
        val = adc(dac)
        GPIO.output(leds, dec2bin(adc()))
        print("Voltage = ", val / levels * maxV)
        #num2str(val)
        voltage_data.append(val / levels * maxV)
        time_data.append(time.time() - start)
    GPIO.output(tryoka, GPIO.LOW)

    while val > 180:
        val = adc(dac)
        print("Voltage = ", val / levels * maxV)
        #num2str(val)
        GPIO.output(leds, dec2bin(adc()))
        voltage_data.append(val / levels * maxV)
        time_data.append(time.time() - start)

    end = time.time()

    with open("settings.txt", 'w') as file:
        file.write(str(end - start) / len(voltage_data)))
        file.write(str(maxV / 256))

    print("duration: ", end - start, " sampling rate: ", len(voltage_data) / (end - start), " ADC quantization step: ", maxV/256)

    GPIO.output(dac, 0)
    GPIO.output(leds, 0)
    GPIO.cleanup()

    time_data_str = [str(i) for i in time_data]
    voltage_data_str = [str(i) for i in voltage_data]

    with open("my_voltage_data.txt", 'w') as file:
        file.write('\n'.join(voltage_data_str))
    with open("my_time_data.txt", 'w') as file:
        file.write('\n'.join(time_data_str))

    plt.plot(time_data, voltage_data)
    plt.show()
except Exception as e:
    print(e)
finally:
    GPIO.cleanup()

