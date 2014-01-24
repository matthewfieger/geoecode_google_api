#################### #################### #################### ####################

# https://developers.google.com/maps/documentation/business/articles/usage_limits #
# https://developers.google.com/maps/documentation/geocoding/

#################### #################### #################### ####################

import urllib # We need this to make requests to an http server.
import json # We need this to parse JSON.
from addresses import addresses # Addresses list in our external addresses.py file.
from addresses import addresses_walgreens # Walgreens list in our external addresses.py file.
from time import sleep # For request throttling

#################### #################### #################### ####################

length =  len(addresses) # Can run for addresses or addresses_walgreens
print "Will reguest geolocation for " + str(length) + " records."

results = 0 # We need this at the bottom to keep track of the number of successful results.


for item in addresses:
   # We want to iterate through each item in our list of addresses, and send a request to Google for each one of those items.
   # Can run for addresses or addresses_walgreens
  attempts = 0 # Our While loop keeps going while this is less than 3.
  success = False  # Our while loop keeps going while this is False.
  address = item[1] # The address is at the second location in our addresses list.
  address = address.replace(" ","+") # Take the spaces out of the address string.
  url = "http://maps.googleapis.com/maps/api/geocode/json?address="+str(address)+"&sensor=false"  # The URL for the Google Geocoding API.
  
  while success != True and attempts < 3:
    # We can throttle our requests with a while loop.
    raw_result = urllib.urlopen(url) # Make the request for the URL.
    raw_result = json.load(raw_result) # Use the JSON plugin to parse the response.
    attempts += 1 # Increment the number of attempts we have made.
    status = raw_result["status"] # Parse the JSON to get the stutus of the response.
    
    if status == "OVER_QUERY_LIMIT":
      # If Google says we have made too many requests, we should wait two seconds and try again.
      sleep(2) # From the time library.
      continue # Retry.

    else:
      # If we are not over our limit, let's keep going.
    	success = True

  if attempts == 3:
    # Send an alert as this means that the daily limit has been reached.
    print "Daily limit has been reached"
    break

  # Capture any other unwanted response we might get.
  elif status != "OK":
    print str(["ERROR", item[0], item[1]]) + ",\n"


  else:
    # And finally we parse a successful response.
    try:
      location = raw_result["results"][0]["geometry"]["location"] # A dictionary that includes both the latitude and the longitude.
      lat = location["lat"] # The key / value for the latidude.
      lng = location["lng"] # The key  / valye for the longitude.
      output = str([lat, lng, item[0], item[1]])+",\n" # We want to output a JS list so that we can display it with Google Maps.
      print output # Print it, or change this to write to a file or database table.
      results += 1 # Keep a count so that we know how many successful requests we had.
    except:
      print str(["ERROR", item[0], item[1]]) + ",\n"

#At the very end print out a report of how things went.
print "Found " + str(results) + " results of " + str(length) + " total."
print "That means that there were " + str(length - results) + " requests that didn't work.  You might want to check on those.\n"

#################### #################### #################### ####################
# Future Upgrades:
  # Print to file or database table.
  # Print separate list for errors.
  # Print directly to an HTML file that will display the locations.

#################### #################### #################### ####################
# For a tutorial on how to display this data with google maps, see:
    # <!-- https://developers.google.com/chart/interactive/docs/gallery/map -->
