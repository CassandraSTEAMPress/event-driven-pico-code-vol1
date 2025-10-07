"""
webserver_HelloBlinky.py
--------
Socket-based web server for turning an LED ON and OFF
  
"""
import gc, sys, socket
from machine import Pin, ADC, reset
from time import sleep, time, localtime
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

# Construct HTML page
def webpage(time_local, temp_celsius, free_memory, led_state):
    # Template HTML
    html = f"""
        <!DOCTYPE html>
        <html>
        <head> <title>Pico W</title> </head>
        <body> <h1>Hello, Blinky!!</h1>
        <form action="./light_on">
        <input type="submit" value="Turn LED on" />
        </form>
        <form action="./light_off">
        <input type="submit" value="Turn LED off" />
        </form>
        <p>LED is {led_state}</p>
        <p>Local Date/Time: {time_local}</p>
        <p>Temperature: {temp_celsius}</p>
        <p>Memory Available: {free_memory}</p>
        </body>
        </html>
        """
    return str(html)

# Set up external LED
led = Pin(16, Pin.OUT)  # GPIO16

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

        # Get the time
        time_unix  = time() # Unix epoch time
        time_local = "%4d/%02d/%02d %02d:%02d:%02d" \
                     % localtime(time_unix)[:6]

        # Get the core temperature of the microcontroller
        temp_reading = temperature_sensor.read_u16() \
                       * conversion_factor
        temp_celsius = 27 - (temp_reading - 0.706)/0.001721
        temp_celsius = "{:,.1f} C".format(temp_celsius)

        # Get the number of bytes of available heap RAM
        gc.collect()
        free_memory = gc.mem_free()

        # Check if led has been turned on or off
        led_on  = request.find('/light_on')
        led_off = request.find('/light_off')
        
        led_state = ""
        if led_on == 6:
            # print("led on")
            led.value(1)
            led_state = "ON"

        if led_off == 6:
            # print("led off")
            led.value(0)
            led_state = "OFF"
            
        # Generate the HTML page
        html = webpage(time_local, \
                       temp_celsius, \
                       free_memory, \
                       led_state)
        
        # Respond to the HTTP request with the HTML page
        #   HTTP status code: 200 for OK
        #   Content is an HTML markup document
        client_socket.send('HTTP/1.1 200 OK\r\n')
        client_socket.send('Content-type: text/html\r\n\r\n')
        client_socket.send(html)
        
        # Close socket connection with the client
        client_socket.close()
        sleep(1)  # delay

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
