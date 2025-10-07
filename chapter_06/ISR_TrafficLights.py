"""
ISR_TrafficLights.py
--------
Simple LED Traffic Light with active Piezo crosswalk buzzer using
    button interrupts

Traffic Light Logic Flow::
  No Pedestrian:
      Red -> Green, Green -> Yellow -> Red
  Pedestrian Crossing:
      Setting the interrupt_flag variable = 1 indicates that
          the crosswalk button was pressed 
      On next Red, buzz for 5 seconds allowing pedestrian to
          cross then set interrupt_flag = 0 and proceed to
          No Pedestrian sequence

"""
from machine import Pin
from time import sleep, ticks_ms, ticks_diff

# Set up LED traffic lights
led_RED    = Pin(16, Pin.OUT)  # GPIO16
led_YELLOW = Pin(17, Pin.OUT)
led_GREEN  = Pin(18, Pin.OUT)

# Set up GPIO pins connected to the crosswalk buzzer and button
buzzer = Pin(14, Pin.OUT)              # GPIO14
button = Pin(15, Pin.IN, Pin.PULL_UP)  # GPIO15

# Define an ISR callback function for a crosswalk button press
interrupt_flag = 0
last_debounce_time = 0
def button_isr(pin):
    global interrupt_flag, last_debounce_time
    current_time = ticks_ms()  # get current time in milliseconds
    
    # Debounce: Has the button been held down for at least 50ms?
    if ticks_diff(current_time, last_debounce_time) > 50:
        interrupt_flag = 1  # set interrupt flag
        last_debounce_time = current_time

# Initialize the IRQ
button.irq(trigger = Pin.IRQ_FALLING, handler = button_isr)  

# LED Traffic Light Controller
def main_program(light_duration = 4):
    global interrupt_flag
    
    button_counter = 0  # the button has not yet been pressed
    while True:
        # Crosswalk button pressed?
        if interrupt_flag == 1:
            # Clear the interrupt flag for the next button press
            interrupt_flag = 0
            
            # Increment crosswalk button counter
            button_counter = button_counter + 1  
            print(f"Crosswalk button counter = {button_counter}")
            
            # Turn red light on for the pedestrians to cross
            led_RED.value(1)  
            
            # Make buzzing sound for 5 seconds
            #     while the pedestrians cross
            for i in range(10):
                buzzer.value(1)
                sleep(0.2) 
                buzzer.value(0)
                sleep(0.2)

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
    
if __name__ == '__main__':
    try:
        # Start main program
        main_program(light_duration = 4)
       
    # Keyboard interrupt caught
    except KeyboardInterrupt:
        print("\nUser interrupted the program.")
        
    # Unexpected error
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    # End the program gracefully
    finally:
        # Turn off traffic light LEDs
        led_RED.off()
        led_YELLOW.off()
        led_GREEN.off()
        
        print("\nISR Pelican Traffic Light"
              " Controller program ended.")
