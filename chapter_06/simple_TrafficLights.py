"""
simple_TrafficLights.py
--------
Simple LED Traffic Lights, no crosswalk

Traffic Light Logic Flow::
      Red -> Green, Green -> Yellow -> Red

"""
from machine import Pin
from time import sleep

# Set up LED traffic lights
led_RED    = Pin(16, Pin.OUT)  # GPIO16
led_YELLOW = Pin(17, Pin.OUT)
led_GREEN  = Pin(18, Pin.OUT)

# LED Traffic Controller
light_duration = 4  # seconds
while True:
    # Red light
    led_RED.value(1)
    sleep(light_duration)
    led_RED.value(0)

    # Green light
    led_GREEN.value(1)
    sleep(light_duration)
    led_GREEN.value(0)
    
    # Yellow light
    led_YELLOW.value(1)
    sleep(light_duration // 2)
    led_YELLOW.value(0)
