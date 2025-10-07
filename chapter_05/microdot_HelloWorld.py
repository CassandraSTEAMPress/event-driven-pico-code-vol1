"""
microdot_HelloWorld.py
--------
Microdot webserver for greeting the world
  
"""
import asyncio, sys
from microdot import Microdot
import connect_wifi

# Add my_secrets.py to the .gitignore file to make sure
#   that my_secrets.py is never checked into GitHub 
import my_secrets
ssid = my_secrets.SSID          # Your SSID (Network Name)
password = my_secrets.PASSWORD  # Your Wi-Fi PASSWORD

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

# Plain text response
@app.get('/')
async def index(request):
    return 'Hello'
# http://[the ip address of your Pico]/
# returns: 'Hello'

# Dictionary response
@app.get('/hello')
async def hello(request):
    return {'Hello': 'world!'}
# http://[the ip address of your Pico]/hello
# returns: {'Hello': 'world!'}

# List response
@app.get('/people')
async def people(request):
    return ["John", "Anna", "Peter"]
# http://[the ip address of your Pico]/people
# returns: ["John","Anna","Peter"]

# Dictionary / List response
@app.get('/hello/people')
async def people(request):
    people_list = ["John", "Anna", "Peter"]
    return {'Hello': people_list}
# http://[the ip address of your Pico]/hello/people
# returns: {"Hello":["John","Anna","Peter"]}

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
        app.shutdown()
        print("\nMicrodot server stopped.")