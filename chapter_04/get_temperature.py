# get_temperature.py - Display flash info, time, and temperature
#   of the microcontroller

import gc
from os import statvfs
from machine import ADC
from time import sleep, time, localtime

# Get the number of bytes of available heap RAM
gc.collect()
free_memory = gc.mem_free()

# Display the amount of free RAM on the console
KB = 1024
print("Free Memory Size: {:,} bytes, {:,.1f} KB".\
      format(free_memory, free_memory / KB))

# Get flash memory size and storage consumption
flash_status = statvfs("/")
flash_size = flash_status[1] * flash_status[2]
flash_free = flash_status[0] * flash_status[3]
flash_used = flash_size - flash_free
    
# Display the flash file system stats on the console
print("File System Size: {:,} bytes, {:,.1f} KB".\
      format(flash_size, flash_size / KB))
print("File System Used: {:,} bytes, {:,.1f} KB".\
      format(flash_used, flash_used / KB))
print("File System Free: {:,} bytes, {:,.1f} KB\n".\
      format(flash_free, flash_free / KB))

# Set up ADC internal temperature reading
temperature_sensor = ADC(ADC.CORE_TEMP)
conversion_factor = 3.3 / (65535)

while True:
    # Get the Unix time and local time
    time_unix  = time() # Unix epoch time
    time_local = "%4d/%02d/%02d %02d:%02d:%02d" \
                 % localtime(time_unix)[:6]

    # Get the core temperature of the microcontroller
    temp_reading = temperature_sensor.read_u16() \
                   * conversion_factor
    tempCelsius = 27 - (temp_reading - 0.706)/0.001721
    tempFahrenheit = 1.8 * tempCelsius + 32
    
    # Display temperature on the console
    print("{}, {}, {:,.1f} C, {:,.1f} F". \
      format(time_unix, time_local, tempCelsius, tempFahrenheit))

sleep(1)  # delay 
