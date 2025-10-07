"""
microdot_HelloName.py
--------
Microdot webserver for greeting people by name
  
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
    print('WiFi authentication error: {}'.\
          format(connect_wifi.SSID_ERROR))
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
# http://[the ip address of your Pico]
# returns: "Hello"

@app.get('/hello')
async def hello(request):
    return {'Hello': 'world!'}
# http://[the ip address of your Pico]/hello
# returns: {"Hello": "world!"}

# List response
@app.get('/people')
async def people(request):
    return ["John", "Anna", "Peter"]
# http://[the ip address of your Pico]/people
# returns: ["John", "Anna", "Peter"]

# Route Parameters
# ----------------
# string (default type): string
@app.get('/hello/<string:name>')
async def hello(request, name):
    return {'Hello': '{}!'.format(name)}
# http://[the ip address of your Pico]/hello/Anna
# returns: {"Hello": "Anna!"}

# re: regular expression (must be valid or the route won't match)
@app.get('/user/<re:[a-zA-Z0-9]*:username>')
async def get_user(request, username):
    return {'User': username}
# http://[the ip address of your Pico]/user/AnnaSmith2
# returns: {"User": "AnnaSmith2"}

# path: remainder of the URL as a path
@app.get('/syslogs/<path:log_path>')
async def get_syslogs(request, log_path):
    return {'syslogs path': log_path}
# http://[the ip address of your Pico]/syslogs//var/log
# returns: {"syslogs path": "/var/log"}

# Parameter combinations
#   int: integer (must be a valid integer
#        or the route won't match)
@app.get('/user/<string:first_name>/<string:last_name>/<int:id>')
async def get_user(request, first_name, last_name, id):
    person = {
                "First Name": first_name,
                "Last Name": last_name,
                "ID": id
             }
    return person
# http://[the ip address of your Pico]/user/Peter/Jones/3
# returns: {"Last Name": "Jones", "ID": 3, "First Name": "Peter"}

# Query parameters
# ----------------
# Individual Query Parameters:
#   param-value pairs separated by ampersands (&)
#   /my_endpoint?param1=value1&param2=value2
@app.get('/greet')
async def greet_person(request):
  # Get query parameters from the request object
  # Get 'name' or default to 'world!'
  name = request.args.get('name', 'world!')
  
  # Get 'message' or default to 'Hello'
  message = request.args.get('message', 'Hello') 

  return {'message': message, 'name': name}
# http://[the ip address of your Pico]/greet?name=Anna
#   returns: {"message": "Hello", "name": "Anna"}

#http://[the ip address of your Pico]/greet?name=Peter&message=Hi
#   returns: {"message": "Hi", "name": "Peter"}
# http://[the ip address of your Pico]/greet
#   returns: {"message": "Hello", "name": "world!"} 

# MultiDict Query Parameters for Multiple Values
#   list of all values associated with a specific parameter
#   /my_endpoint?param=value1&param=value2
@app.get('/greet/people')
async def greet_people(request):
    # Get all values for the parameter 'name'
    peoples_names = request.args.getlist('name')
    
    # Get 'message' or default to 'Hello'    
    message = request.args.get('message', 'Hello') 

    return {'message': message, 'people': peoples_names}
# http://[the ip address of your Pico]
# /greet/people?name=John&name=Anna&name=Peter
#   returns: {"message": "Hello",
#              "people": ["John", "Anna", "Peter"]}
# http://[the ip address of your Pico]
# /greet/people?message=Welcome&name=John&name=Anna&name=Peter
#   returns: {"message": "Welcome",
#             "people": ["John", "Anna", "Peter"]}

# Main entry point for the event loop
async def main():
    print("Starting async task ...")
    await app.start_server(host=ip_address, port=80, debug=True)
    
if __name__ == '__main__':

    # Start event loop
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