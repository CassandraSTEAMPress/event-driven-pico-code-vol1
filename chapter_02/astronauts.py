# astronauts.py - Show people in space and their location
#   (400km / ~250 miles overhead)
#   see: http://open-notify.org/,
#        https://github.com/open-notify/Open-Notify-API

import requests, sys

# Add my_secrets.py to the .gitignore file to make sure
#   that my_secrets.py is never checked into GitHub 
import my_secrets
ssid = my_secrets.SSID          # Your SSID (Network Name)
password = my_secrets.PASSWORD  # Your WiFi PASSWORD

# Initialize the WiFi Interface
import connect_wifi
if not connect_wifi.init_wlan( \
                              ssid, \
                              password, \
                              max_retries=10):
    print('WiFi authentication error: {}'\
          .format(connect_wifi.SSID_ERROR))
    print('Exiting program')
    sys.exit(0)
else:
    ip_address = connect_wifi.get_ip()
    
# Request the JSON data for the astronauts currently in space
astronauts_URL = "http://api.open-notify.org/astros.json"
astronauts = requests.get(astronauts_URL, \
                          timeout=10)  # 10-second timeout

# Show people in space and their spacecraft if the HTTP \
#   response is successful
if astronauts.status_code == 200:  # (200 = OK)
    print(f"\nastronauts_in_space = {astronauts.json()}")
else:
    print("Unable to fetch astronaut data.")

# Close the connection to the server to release network resources
astronauts.close()
    
# Request the JSON data for the ISS location
iss_URL = "http://api.open-notify.org/iss-now.json"
iss_now = requests.get(iss_URL, timeout=10)  # 10-second timeout

# Show ISS location if the HTTP response is successful
if iss_now.status_code == 200:  # (200 = OK)
    print(f"\nISS_position_and_time = {iss_now.json()}")
else:
    print("Unable to fetch ISS position and time.")

# Close the connection to the server to release network resources
iss_now.close()