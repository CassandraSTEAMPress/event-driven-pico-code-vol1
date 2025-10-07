# sunrise.py - Show the current ISS location and the sunrise and
#   sunset times on the ground immediately below that location
import requests, sys

# Add my_secrets.py to the .gitignore file to make sure
#   that my_secrets.py is never checked into GitHub 
import my_secrets
ssid = my_secrets.SSID          # Your SSID (Network Name)
password = my_secrets.PASSWORD  # Your WiFi PASSWORD

# Initialize the WiFi Interface
import connect_wifi
if not connect_wifi.init_wlan(ssid, password, max_retries=10):
    print('WiFi authentication error: {}'\
          .format(connect_wifi.SSID_ERROR))
    print('Exiting program')
    sys.exit(0)
else:
    ip_address = connect_wifi.get_ip()

try: 
    # Request the JSON data for the ISS location
    iss_URL = "http://api.open-notify.org/iss-now.json"
    iss_now = requests.get(iss_URL, timeout=10)  # 10-sec timeout

    # Get ISS location if the HTTP response is successful
    if iss_now.status_code == 200:
        print("\nCurrent_ISS_position_and_time:")
        json_data = iss_now.json()
        
        # Format and display the JSON data 
        json_niceify = "{\n"
        for key, value in json_data.items():
            json_niceify += f'  "{key}": "{value}",\n'
        json_niceify = json_niceify.rstrip(",\n") + "\n}"
        print(f"json_data = {json_niceify}")
            
        iss_latitude  = json_data["iss_position"]["latitude"]
        iss_longitude = json_data["iss_position"]["longitude"]
        iss_location = f"{iss_latitude},{iss_longitude}"

    else:
        print("Unable to fetch ISS position and time.")
        
    # Release network resources
    if iss_now:
        iss_now.close()  
    
    # Get the sunrise and sunset times for the ISS location
    sunrise_URL = "https://api.sunrise-sunset.org/json?lat=" \
                + iss_latitude + "&lng=" + iss_longitude
    sunrise_now = requests.get(sunrise_URL, timeout=10)  

    # Show the sunrise and sunset times 
    #   if the HTTP response is successful
    if sunrise_now.status_code == 200: 
        json_data = sunrise_now.json()
        print("\nSunrise and sunset times:")
        print("(JSON data from https://api.sunrise-sunset.org)")
        print(f"sunrise     = {json_data["results"]["sunrise"]}")
        print(f"sunset      = {json_data["results"]["sunset"]}")
        print(f"day length  = {\
                              json_data["results"]["day_length"]\
                              }")
        
    else:
        print("Unable to fetch sunrise and sunset times.")
    
    # Release network resources
    if sunrise_now:
        sunrise_now.close()  
    
# Keyboard interrupt caught
except KeyboardInterrupt:
    print("\nUser interrupted the program")

# JSON decoding error?
except ValueError as e:
    print(f"JSON decoding error: {e}")

# Catch other potential errors, e.g., network errors
except Exception as e: 
    print(f"An unexpected error occurred: {e}")

finally:   
    print("\nProgram ended.")
    