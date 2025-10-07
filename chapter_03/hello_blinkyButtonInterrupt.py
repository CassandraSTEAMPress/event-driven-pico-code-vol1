# hello_blinkyButtonInterrupt.py - Blink an external LED with
#   a button interrupt
from machine import Pin
from time import sleep, ticks_ms, ticks_diff

# Initialize the LED
led = Pin(16, Pin.OUT)  # GPIO16
led.off()

# Initialize the button pin
button = Pin(15, Pin.IN, Pin.PULL_UP)  # GPIO15

# Define an ISR callback function for a button press
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

# Perform main tasks while the IRQ is running in the background
def main_program():
    global interrupt_flag
    while True:
        # Button pressed?
        if interrupt_flag == 1:
            print("Button press detected!")
            led.toggle()  # toggle LED
            interrupt_flag = 0  # reset interrupt flag
        sleep(1)  # delay

if __name__ == '__main__':
    try:
        # Start main program
        main_program()
       
    # Keyboard interrupt caught
    except KeyboardInterrupt:
        print("\nUser interrupted the program.")
        
    # Unexpected error
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    # End the program gracefully
    finally:
        # Turn off LED
        led.off()
        
        print("\nButton interrupt program ended.")