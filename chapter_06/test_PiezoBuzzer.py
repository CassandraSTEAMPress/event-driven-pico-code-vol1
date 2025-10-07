"""
test_PiezoBuzzer.py
--------
Check that Active Piezo Buzzer makes a sound

"""
from machine import Pin
from time import sleep

# Set up active Piezo buzzer
buzzer = Pin(14, Pin.OUT)  # GPIO14

for i in range(10):
    buzzer.value(1)
    sleep(0.2)
    buzzer.value(0)
    sleep(0.2)
