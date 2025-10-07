# hello_blinkyTimerInterrupt.py - Blink an external LED with a
#   periodic timer interrupt

from machine import Pin, Timer
from time import sleep

# Initialize the LED
led = Pin(16, Pin.OUT)  # GPIO16
led.off()

# Define an ISR callback function for when the timer triggers
def timer_isr(timer_obj):
    led.toggle()

# Initialize a periodic timer
led_timer = Timer(-1) # Create a virtual timer (id=-1)
led_timer.init(mode=Timer.PERIODIC, period=250, \
               callback=timer_isr)

# Perform main tasks while the timer is running in the background
def main_program():
    counter = 0
    while True:      
        if counter % 5 != 0:
            print('.', end='')
        else:
            print(counter, end='')
            
        counter += 1
        sleep(1)

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
        # Stop the timer
        print('\nDeinitializing timer')
        led_timer.deinit()

        # Turn off LED
        led.off()
        
        print("\nPERIODIC timer interrupt program ended.")
