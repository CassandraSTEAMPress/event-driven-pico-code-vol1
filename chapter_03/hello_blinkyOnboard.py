# hello_blinkyOnboard.py - Blink the onboard LED every second

from machine import Pin
from time import sleep

# Initialize the onboard LED
led = Pin("LED", Pin.OUT)
led.off()

# Toggle LED
def toggle_LED():
    while True:
        led.toggle()  # turn the LED on if it's off
                      # turn it off if it's on
        sleep(1)  # delay 1 second
    
if __name__ == '__main__':
    try:
        # Start blinking the LED
        toggle_LED()
       
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
        
        print("\nOnboard LED blinking program stopped.")