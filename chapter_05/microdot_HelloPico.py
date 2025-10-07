"""
microdot_HelloPico.py
--------
Microdot webserver for turning an LED ON and OFF
    + Event information
    
"""
import gc
from machine import Pin, ADC
import asyncio, sys
from microdot import Microdot, Response
from time import time, localtime
import connect_wifi, pico_event

# Add my_secrets.py to the .gitignore file to make sure
#   that my_secrets.py is never checked into GitHub 
import my_secrets
ssid = my_secrets.SSID          # Your SSID (Network Name)
password = my_secrets.PASSWORD  # Your Wi-Fi PASSWORD

# Set up external LED
led = Pin(16, Pin.OUT)  # GPIO16

# Set up ADC internal temperature reading
temperature_sensor = ADC(ADC.CORE_TEMP)
conversion_factor = 3.3 / (65535)

# Initialize the WiFi Interface
if not connect_wifi.init_wlan(ssid, password, max_retries=10):
    print('WiFi authentication error: {}'\
          .format(connect_wifi.SSID_ERROR))
    print('Exiting program')
    sys.exit(0)
else:
    ip_address = connect_wifi.get_ip()
    
# Instantiate a Microdot webserver
app = Microdot()

# Microdot communications interface
@app.get('/')
async def index(request):
    return 'Hello'

led_state = "OFF"
def webpage(time_local, temp_celsius, free_memory, led_state):
    # Template HTML
    html = f"""
    <!doctype html>
    <html>
        <head><title>Hello, Pico!</title></head>
        <body>
            <h1>Hello, Pico!</h1>
            <form method="POST">
                <button type="submit" name="led_on">\
                    Turn LED on</button><br/>
                <button type="submit" name="led_off">\
                    Turn LED off</button>
            </form>
            
            <p>LED is {led_state}</p>
            <p>Local Date/Time: {time_local}</p>
            <p>Temperature: {temp_celsius}</p>
            <p>Memory Available: {free_memory}</p>
        </body>
    </html>
    """
    return str(html)

@app.route('/api/v0.1/light_switch', methods=['GET', 'POST'])
async def light_switch(request):
    # Initialize the LED light to off
    led.value(0)  
    led_state = "OFF"

    # Turn LED light on if the client sent
    #   a POST request to turn on the LED
    if request.method == 'POST':
        if 'led_on' in request.form:
            led.value(1)  
            led_state = "ON"

    # Get the Unix epoch time as well as the local time
    time_unix  = time()  # Unix epoch time
    time_local = "%4d/%02d/%02d %02d:%02d:%02d" \
                 % localtime(time_unix)[:6]

    # Get the core temperature of the microcontroller
    temp_reading = temperature_sensor.read_u16() \
                   * conversion_factor
    temp_celsius = 27 - (temp_reading - 0.706)/0.001721
    temp_celsius = "{:,.1f} C".format(temp_celsius)

    # Check the number of bytes of available heap RAM
    KB = 1024
    gc.collect()
    free_memory = gc.mem_free()
    free_memory = "{:,.1f} KB".format(free_memory/KB)
        
    # Generate the HTML form
    html =  webpage(time_local, \
                    temp_celsius, \
                    free_memory, \
                    led_state)

    # Respond to the HTTP request with the HTML form
    #   HTTP status code: 200 for OK
    #   Content is an HTML markup document
    return Response(html, status_code=200, \
                    headers={'Content-Type': 'text/html'})

@app.get('/api/v0.1/light/on')
async def light_on(request):
    led.value(1)
    event_header = pico_event.header()
    event_body   = {
                     'led_state': 'ON',
                     'hardware_parameters': \
                          pico_event.hardware_parameters()
                   }
    return {"header": event_header, "body": event_body}
# http://[the ip address of your Pico]/api/v0.1/light/on
#   returns: event header and body with led_state = ON

@app.get('/api/v0.1/light/off')
async def light_off(request):
    led.value(0)
    event_header = pico_event.header()
    event_body   = {
                     'led_state': 'OFF',
                     'hardware_parameters': \
                          pico_event.hardware_parameters()
                   }
    return {"header": event_header, "body": event_body}
# http://[the ip address of your Pico]/api/v0.1/light/off
#   returns: event header and body with led_state = OFF

# Route Parameter: LED state must be an integer
@app.get('/api/v0.1/light/<int:state>')
async def light_state(request, state):
    if state != 0:  # turn LED ON for non-zero state
        led_state = "ON"
        led.value(1)
    else:
        led_state = "OFF"
        led.value(0)

    event_header = pico_event.header()
    event_body   = {
                     'led_state': led_state,
                     'hardware_parameters': \
                         pico_event.hardware_parameters()
                   }
    return {"header": event_header, "body": event_body}
# http://[the ip address of your Pico]/api/v0.1/light/1
# http://[the ip address of your Pico]/api/v0.1/light/0
#   returns: event header and body with led_state = ON or OFF

# Query Parameter: LED state must be either "ON" or "OFF"
@app.get('/api/v0.1/light')
async def light_state(request):
    # Get query parameters from the request object
    
    # Get 'state' or default to 'Unknown'
    led_state = request.args.get('state', 'Unknown') 
    if (led_state != 'ON') and (led_state != 'OFF'):
        raise ValueError(\
            f"led_state = {led_state} (must be 'ON' or 'OFF')")

    if led_state == 'ON':
        led.value(1)
    else:
        led.value(0)
        
    event_header = pico_event.header()
    event_body   = {
                     'led_state': led_state,
                     'hardware_parameters': \
                         pico_event.hardware_parameters()
                   }
    return {"header": event_header, "body": event_body}
# http://[the ip address of your Pico]/api/v0.1/light?state=ON
# http://[the ip address of your Pico]/api/v0.1/light?state=OFF
#   returns: event header and body with led_state = ON or OFF

# Main entry point for the event loop
async def main():
    print("Starting async task ...")
    await app.start_server(host=ip_address, port=80, debug=True)
    
# Start the event loop
if __name__ == '__main__':

    try:
        # Run the Microdot webserver
        print("Starting Microdot server ...")
        main_task=asyncio.run(main())
       
    # Keyboard interrupt caught
    except KeyboardInterrupt:
        print("\nUser interrupted the program")
        
    # Unexpected error
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    # End the program gracefully
    finally:
        # Turn off LED
        led.value(0)
        app.shutdown()
        print("\nMicrodot server stopped.")