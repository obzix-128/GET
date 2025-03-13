import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt

# Настройка пинов
dac = [8, 11, 7, 1, 0, 5, 12, 6]  # Пины для ЦАП
comp = 14  # Пин для компаратора
troyka = 13  # Пин для управления Troyka-модулем
leds = [2, 3, 4, 17, 27, 22, 10, 9]  # Пины для светодиодов

# Настройка GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial=0)
GPIO.setup(comp, GPIO.IN)
GPIO.setup(leds, GPIO.OUT)

# Функция для преобразования числа в двоичный список
def decimal_to_binary_list(n):
    return [int(bit) for bit in bin(n)[2:].zfill(8)]

# Функция для измерения напряжения с помощью АЦП
def adc():
    value = 0
    for i in range(7, -1, -1):
        value += 2**i
        GPIO.output(dac, decimal_to_binary_list(value))
        time.sleep(0.001)  # Уменьшаем задержку для повышения точности
        if GPIO.input(comp) == 1:
            value -= 2**i
    return value

# Функция для включения светодиодов в зависимости от значения
def light_up(value):
    num_led = int(value / 256.0 * 8)
    for i in range(8):
        GPIO.output(leds[i], 1 if i < num_led else 0)

# Функция для измерения напряжения на Troyka-модуле
def measure_voltage():
    return adc() * 3.3 / 256.0

# Основной блок
try:
    measurements = []  # Список для хранения измерений
    start_time = time.time()  # Запись времени начала измерений

    # Зарядка конденсатора
    GPIO.output(troyka, 1)  # Подаем 3.3В на Troyka-модуль
    print("Начало зарядки конденсатора")
    while True:
        voltage = measure_voltage()
        measurements.append(voltage)
        light_up(int(voltage / 3.3 * 255))
        if voltage >= 3.3 * 0.97:  # Остановка при достижении 97% от 3.3В
            break
        time.sleep(0.01)

    # Разрядка конденсатора
    GPIO.output(troyka, 0)  # Подаем 0В на Troyka-модуль
    print("Начало разрядки конденсатора")
    while True:
        voltage = measure_voltage()
        measurements.append(voltage)
        light_up(int(voltage / 3.3 * 255))
        if voltage <= 3.3 * 0.02:  # Остановка при достижении 2% от 3.3В
            break
        time.sleep(0.01)

    end_time = time.time()  # Запись времени завершения измерений
    duration = end_time - start_time  # Продолжительность эксперимента

    # Сохранение данных в файл data.txt
    with open("data.txt", "w") as file:
        for value in measurements:
            file.write(f"{value}\n")

    # Расчет средней частоты дискретизации и шага квантования
    sampling_rate = len(measurements) / duration
    quantization_step = 3.3 / 256.0

    # Сохранение настроек в файл settings.txt
    with open("settings.txt", "w") as file:
        file.write(f"Средняя частота дискретизации: {sampling_rate:.2f} Гц\n")
        file.write(f"Шаг квантования АЦП: {quantization_step:.4f} В\n")

    # Построение графика
    plt.plot(measurements)
    plt.title("Зависимость напряжения от времени")
    plt.xlabel("Номер измерения")
    plt.ylabel("Напряжение, В")
    plt.show()

    # Вывод информации в терминал
    print(f"Общая продолжительность эксперимента: {duration:.2f} с")
    print(f"Период одного измерения: {duration / len(measurements):.4f} с")
    print(f"Средняя частота дискретизации: {sampling_rate:.2f} Гц")
    print(f"Шаг квантования АЦП: {quantization_step:.4f} В")

finally:
    # Сброс GPIO
    GPIO.output(dac, 0)
    GPIO.output(troyka, 0)
    GPIO.output(leds, 0)
    GPIO.cleanup()
