"""
microdot_TrafficLights.py
--------
Pelican LED Traffic Lights with active Piezo crosswalk buzzer
    and push button using ISR

Traffic Light Logic Flow::
  No Pedestrian:
    Red -> Green, Green -> Yellow -> Red
  Pedestrian Crossing:
    Pressing the crosswalk button (config.button_pressed = True)
        indicates that a pedestrian wishes to cross
    On next Red, buzz for 5 seconds allowing pedestrian to cross
        then set config.button_pressed = False and proceed to
        No Pedestrian sequence

Use a Microdot webserver to provide data consumers with
  event details

"""
from machine import Pin
from time import sleep
import asyncio, webserver_TrafficLights, config

# Set up LED traffic lights
led_RED    = Pin(16, Pin.OUT)  # GPIO16
led_YELLOW = Pin(17, Pin.OUT)
led_GREEN  = Pin(18, Pin.OUT)

# Set up GPIO pins connected to the crosswalk buzzer and button
crosswalk_buzzer = Pin(14, Pin.OUT)              # GPIO14
crosswalk_button = Pin(15, Pin.IN, Pin.PULL_UP)  # GPIO15

# Turn off LEDs
def turn_off_lights():
    print("Turning off lights")
    led_RED.value(0)     # Red light    OFF
    led_GREEN.value(0)   # Green light  OFF
    led_YELLOW.value(0)  # Yellow light OFF

# Asyncio flags to signal button press from ISR to asyncio task
button_pressed_flag = asyncio.ThreadSafeFlag()
button_pressed_event = asyncio.Event()

# Interrupt Service Routine (ISR) that sets the flag to signal
#     the handle_button_press() coroutine
def button_isr(pin):
    button_pressed_flag.set()

# Bridging ISR to asyncio event loop
async def handle_button_press():
    while True:
        # Wait for the button pressed flag to be set by the ISR
        await button_pressed_flag.wait()
        
        # Debounce the button for at least 50 ms to prevent
        #   multiple triggers from a single press
        await asyncio.sleep_ms(50)

        # Check button state again after debouncing the buttton
        if crosswalk_button.value() == 0:
            print("Button pressed!")
            button_pressed_event.set()

# LED Traffic Lights Controller
async def traffic_lights(light_duration = 4):
    """Simulate a Pelican traffic light using asyncio"""

    config.button_counter = 0
    while True:
        # If crosswalk button is pressed, clear
        #   the event for the next button press
        if button_pressed_event.is_set():
            button_pressed_event.clear()
            
            # Pedestrians are in crosswalk
            config.button_pressed = True  
            
            # Increment button counter
            config.button_counter = config.button_counter + 1
            
            print(f"Crosswalk button counter = "
                  f"{config.button_counter}")                            
            led_RED.value(1)
            
            # Make buzzing sound for 5 seconds
            #     while the pedestrians cross
            for i in range(10):
                crosswalk_buzzer.value(1)
                sleep(0.2) 
                crosswalk_buzzer.value(0)
                sleep(0.2)
                await asyncio.sleep_ms(100)
                
            # Pedestrians have crossed the road
            config.button_pressed = False  
            
        # Red light
        led_RED.value(1)
        await asyncio.sleep(light_duration)
        led_RED.value(0)

        # Green light
        led_GREEN.value(1)
        await asyncio.sleep(light_duration)
        led_GREEN.value(0)
        
        # Yellow light
        led_YELLOW.value(1)
        await asyncio.sleep(light_duration // 2)
        led_YELLOW.value(0)

# Main entry point for the event loop
async def main():
    print("Starting async tasks ...")
    
    # Attach the interrupt handler to the button pin
    crosswalk_button.irq(trigger=Pin.IRQ_FALLING, \
                         handler=button_isr)
    
    # Create the button handling task
    button_task = \
                asyncio.create_task(handle_button_press())
    
    # Create the web server handling task
    web_server = asyncio.create_task(\
        webserver_TrafficLights.start_server())

    # Create traffic lights task
    traffic_controller_task = \
        asyncio.create_task(traffic_lights(light_duration = 4))

    # Schedule asyncio tasks to be run concurrently as a group
    await asyncio.gather(button_task, \
                         traffic_controller_task, \
                         web_server)

if __name__ == "__main__":
    
    # Start event loop
    try:
        main_task=asyncio.run(main())

    # Keyboard interrupt caught
    except KeyboardInterrupt:
        print("Traffic lights interrupted by user.")

    # Unexpected error
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        
    # Turn off LEDs
    finally:
        # Turn off the traffic lights
        turn_off_lights()

        print("\nMicrodot Pelican Traffic Light Controller "
              "program ended.")