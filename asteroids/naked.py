# Imports requests needed for the project
# Requests - used for requesting data from different HTML places, e.g. API for this project
# Json - here used for fetching the provided data from the API
# Datetime - to fetch the date 
# Time - to fetch time
# Yaml - to access the configuration files

import requests
import json
import datetime
import time
import yaml

# Imports the date and prints text in the console, starts processing the request
from datetime import datetime
print('Asteroid processing service')

# Initiating and reading config values
print('Loading configuration from file')

# Defines the API key with which the asteroid data is accessed
# Uses the URL to get to the data
nasa_api_key = "tpTJMfWQc4JOtXZbpWotfhklh9oTlTirhRnDa1gX"
nasa_api_url = "https://api.nasa.gov/neo/"

# Getting todays date
# .zfill adds a number of zeros to match the needed lenght, it fetches year, month and day
# Prints out the date
dt = datetime.now()
request_date = str(dt.year) + "-" + str(dt.month).zfill(2) + "-" + str(dt.day).zfill(2)  
print("Generated today's date: " + str(request_date))

# Generates the URL with all the fetched data and the API
print("Request url: " + str(nasa_api_url + "rest/v1/feed?start_date=" + request_date + "&end_date=" + request_date + "&api_key=" + nasa_api_key))
r = requests.get(nasa_api_url + "rest/v1/feed?start_date=" + request_date + "&end_date=" + request_date + "&api_key=" + nasa_api_key)

# Prints out the reuqest status code, which has to be 200, otherwise, it is not going to work
# Then prints the headers
# Then the content
print("Response status code: " + str(r.status_code))
print("Response headers: " + str(r.headers))
print("Response content: " + str(r.text))

# Checks if the HTTP code is 200 to parse the data
if r.status_code == 200:

	# Converts the received cntent data for python
	json_data = json.loads(r.text)

	# Defines the safe asteroid list
	# Defines the hazardous asteroid list
	ast_safe = []
	ast_hazardous = []

	# Checks if the needed data is in the received json data
		# Defines the count as the one received from the data
		# Prints the asteroid count, parsed as a string
	if 'element_count' in json_data:
		ast_count = int(json_data['element_count'])
		print("Asteroid count today: " + str(ast_count))

		# Creates an if statement for when the asteroid count today is bigger than 0
		if ast_count > 0:
			for val in json_data['near_earth_objects'][request_date]:
				# Reads the values of the asteroids - the name and then the URL where the asteroid is described
				if 'name' and 'nasa_jpl_url' and 'estimated_diameter' and 'is_potentially_hazardous_asteroid' and 'close_approach_data' in val:
					tmp_ast_name = val['name']
					tmp_ast_nasa_jpl_url = val['nasa_jpl_url']
					# Gets the data for the size of the asteroid, min and max size, otherwise, it sets a specified value
					# Or if there is none to fetch it still sets the specified value
					if 'kilometers' in val['estimated_diameter']:
						if 'estimated_diameter_min' and 'estimated_diameter_max' in val['estimated_diameter']['kilometers']:
							tmp_ast_diam_min = round(val['estimated_diameter']['kilometers']['estimated_diameter_min'], 3)
							tmp_ast_diam_max = round(val['estimated_diameter']['kilometers']['estimated_diameter_max'], 3)
						else:
							tmp_ast_diam_min = -2
							tmp_ast_diam_max = -2
					else:
						tmp_ast_diam_min = -1
						tmp_ast_diam_max = -1

					tmp_ast_hazardous = val['is_potentially_hazardous_asteroid']

					# Data if there are any asteroids that approach close, when the count is bigger than 0
					# Code to determine when the approach is going to happen
					if len(val['close_approach_data']) > 0:
						# strftime - converting the date/time to string

						if 'epoch_date_close_approach' and 'relative_velocity' and 'miss_distance' in val['close_approach_data'][0]:
							tmp_ast_close_appr_ts = int(val['close_approach_data'][0]['epoch_date_close_approach']/1000)
							# The time of approach of the asteroid in UTC 
							tmp_ast_close_appr_dt_utc = datetime.utcfromtimestamp(tmp_ast_close_appr_ts).strftime('%Y-%m-%d %H:%M:%S')
							# The time of approach of the asteroid in local timezone
							tmp_ast_close_appr_dt = datetime.fromtimestamp(tmp_ast_close_appr_ts).strftime('%Y-%m-%d %H:%M:%S')

							# Retrieves the speed of the asteroid
							if 'kilometers_per_hour' in val['close_approach_data'][0]['relative_velocity']:
								tmp_ast_speed = int(float(val['close_approach_data'][0]['relative_velocity']['kilometers_per_hour']))
							else:
								tmp_ast_speed = -1

							# Retrieves the distance missed from the Earth, how close it has come
							if 'kilometers' in val['close_approach_data'][0]['miss_distance']:
								tmp_ast_miss_dist = round(float(val['close_approach_data'][0]['miss_distance']['kilometers']), 3)
							else:
								tmp_ast_miss_dist = -1
						# The idintifaction of the asteroid, as it's approaching close
						else:
							tmp_ast_close_appr_ts = -1
							tmp_ast_close_appr_dt_utc = "1969-12-31 23:59:59"
							tmp_ast_close_appr_dt = "1969-12-31 23:59:59"

					# Data set if the asteroid is not going to approach closely
					else:
						print("No close approach data in message")
						tmp_ast_close_appr_ts = 0
						tmp_ast_close_appr_dt_utc = "1970-01-01 00:00:00"
						tmp_ast_close_appr_dt = "1970-01-01 00:00:00"
						tmp_ast_speed = -1
						tmp_ast_miss_dist = -1

					# Prints info about the asteroid:
					# Name, URL from the nasa site, diameter, if it is hazardous, close approach TS, date/time in UTC
					# then in local time, the speed, the miss distance (close approach)
					print("------------------------------------------------------- >>")
					print("Asteroid name: " + str(tmp_ast_name) + " | INFO: " + str(tmp_ast_nasa_jpl_url) + " | Diameter: " + str(tmp_ast_diam_min) + " - " + str(tmp_ast_diam_max) + " km | Hazardous: " + str(tmp_ast_hazardous))
					print("Close approach TS: " + str(tmp_ast_close_appr_ts) + " | Date/time UTC TZ: " + str(tmp_ast_close_appr_dt_utc) + " | Local TZ: " + str(tmp_ast_close_appr_dt))
					print("Speed: " + str(tmp_ast_speed) + " km/h" + " | MISS distance: " + str(tmp_ast_miss_dist) + " km")
					
					# Adding asteroid data to the corresponding array
					# If by the parameters it is deemed as hazardous then it gets added to the hazardous list, otherwise,
					# it is added to the safe asteroid list
					if tmp_ast_hazardous == True:
						ast_hazardous.append([tmp_ast_name, tmp_ast_nasa_jpl_url, tmp_ast_diam_min, tmp_ast_diam_max, tmp_ast_close_appr_ts, tmp_ast_close_appr_dt_utc, tmp_ast_close_appr_dt, tmp_ast_speed, tmp_ast_miss_dist])
					else:
						ast_safe.append([tmp_ast_name, tmp_ast_nasa_jpl_url, tmp_ast_diam_min, tmp_ast_diam_max, tmp_ast_close_appr_ts, tmp_ast_close_appr_dt_utc, tmp_ast_close_appr_dt, tmp_ast_speed, tmp_ast_miss_dist])

		# The print in case if the asteroid count is 0
		else:
			print("No asteroids are going to hit earth today")

	# Prints the count of the hazardous asteroids and the safe asteroids
	print("Hazardous asteorids: " + str(len(ast_hazardous)) + " | Safe asteroids: " + str(len(ast_safe)))

	# Sorts if the asteroi dis hazardous by the 4th parameter which is TS of close approach
	ast_hazardous.sort(key = lambda x: x[4], reverse=False)

	# Prints the times and info of possible hazardious asteroids today
	print("Today's possible apocalypse (asteroid impact on earth) times:")
	for asteroid in ast_hazardous:
		print(str(asteroid[6]) + " " + str(asteroid[0]) + " " + " | more info: " + str(asteroid[1]))

	# Checks for asteroids by the 8th parameter which is the miss distance and then prints the closest passing distance,
	# with the data for the asteroid
	ast_hazardous.sort(key = lambda x: x[8], reverse=False)
	print("Closest passing distance is for: " + str(ast_hazardous[0][0]) + " at: " + str(int(ast_hazardous[0][8])) + " km | more info: " + str(ast_hazardous[0][1]))

# Error message in case if there were difficulties getting the to the API 
else:
	print("Unable to get response from API. Response code: " + str(r.status_code) + " | content: " + str(r.text))
