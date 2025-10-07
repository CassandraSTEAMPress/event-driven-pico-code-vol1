"""
webserver_HelloPico.py
--------
Socket-based web server that turns an LED ON and OFF
  and responds with an Event
  
"""
import gc, sys, socket
from machine import Pin, unique_id, ADC, reset
from time import sleep, time, localtime
from os import urandom
from json import dumps
import connect_wifi, get_socket

# Add my_secrets.py to the .gitignore file to make sure
#   that my_secrets.py is never checked into GitHub 
import my_secrets
ssid = my_secrets.SSID          # Your SSID (Network Name)
password = my_secrets.PASSWORD  # Your WiFi PASSWORD

# Initialize the WiFi Interface
if not connect_wifi.init_wlan(ssid, password, max_retries=10):
    print('WiFi authentication error: {}'.\
          format(connect_wifi.SSID_ERROR))
    print('Exiting program')
    sys.exit(0)
else:
    # Use Port 80 = default network port number for HTTP
    s = get_socket.init(port=80)  

"""Generate a version 4 UUID compliant to RFC 4122"""
def uuid4():
    random_x = bytearray(urandom(16))
    random_x[6] = (random_x[6] & 0x0F) | 0x40
    random_x[8] = (random_x[8] & 0x3F) | 0x80
    h = random_x.hex()
    return str('-'.join((h[0:8], h[8:12], \
                         h[12:16], h[16:20], h[20:32])))

# Set up external LED
led = Pin(16, Pin.OUT)

# Set up ADC internal temperature reading
temperature_sensor = ADC(ADC.CORE_TEMP)
conversion_factor = 3.3 / (65535)

# Web server using sockets
def handle_client(s):        
    # Listen for connections
    while True:
        # Accept incoming connections
        client_socket, client_address = s.accept()  

        # Receive data from the client
        request = client_socket.recv(1024) 
        request = str(request)
        # print("\n{}".format(request))

        # Get a unique id for this event
        event_id = uuid4()
        # print (event_id)
        
        # Get the time
        time_unix  = time() # Unix epoch time
        time_local = "%4d/%02d/%02d %02d:%02d:%02d" \
                     % localtime(time_unix)[:6]

        # Get the core temperature of the RP2040
        temp_reading = temperature_sensor.read_u16() \
                       * conversion_factor
        temp_celsius = 27 - (temp_reading - 0.706)/0.001721
        temp_celsius = "{:,.1f} C".format(temp_celsius)

        # Check the number of bytes of available heap RAM
        KB = 1024
        gc.collect()
        free_memory = gc.mem_free()
        free_memory = "{:,.1f} KB".format(free_memory/KB)

        # Check if led has been turned on or off
        led_on  = request.find('/light_on')
        led_off = request.find('/light_off')
        
        led_state = ""
        if led_on == 6:
            print("led on")
            led.value(1)
            led_state = "ON"

        if led_off == 6:
            print("led off")
            led.value(0)
            led_state = "OFF"
        
        # Create an Event as a MicroPython dictionary
        xDict = {
            "event_id": event_id,
            "version": 1.01,
            "machine_unique_id": unique_id().hex(),
            "time_unix":    time_unix,
            "time_local":   time_local,
            "temp_celsius": temp_celsius,
            "free_memory":  free_memory,
            
            "led_state":    led_state
        }

        # Convert the Event dictionary into a JSON UTF-8 string 
        resp = dumps(xDict).encode()
        
        # Send response back to client
        client_socket.send('HTTP/1.0 200 OK\r\n')
        client_socket.send(\
            'Content-type: application/json\r\n\r\n')
        client_socket.send(resp)
        
        # close socket connection with the client
        client_socket.close()
        sleep(1)


if __name__ == '__main__':
    try:
        # Start web server
        handle_client(s)
       
    # Keyboard interrupt caught
    except KeyboardInterrupt:
        print("\nUser interrupted the program.")
        
    # Handle the network error
    except OSError as e:
        print("OSError: errno={} {}", format(e.errno, e.args[0]))
    
    # End the program gracefully
    finally:
        print("\nWeb server stopped.")