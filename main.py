import requests
from dotenv import load_dotenv
import os
import datetime

load_dotenv()

# Retrieves data from Api
def pull_earthquake_data():
    url = os.getenv('earthquake_api_link') # fetches url from env variable
    params = {
        "format": "geojson",
        "starttime": "2024-01-01",
        "minmagnitude": 5.0
    }

    response = requests.get(url=url, params=params) # making actual request
    if response.status_code == 200: # check if request was successful
        return response.json() # returns data in json format if the request was successful
    else:
        raise Exception("Failed to fetch data!") # throws error is request failed.

# Separates unwanted data and reformats data and time to human-readable format
def parse_earthquake_data(data):
    parsed_data = [] # Empty list
    for feature in data['features']:
        earthquake = {
            "magnitude": feature['properties']['mag'],
            "location": feature['properties']['place'],
            "time": datetime.datetime.utcfromtimestamp(feature['properties']['time'] / 1000).strftime('%Y-%m-%d %H:%M:%S'),
            "coordinates": feature['geometry']['coordinates'],
            "url": feature['properties']['url']
        }
        parsed_data.append(earthquake)
    return parsed_data

# Fetches data over specified parameters
def filter_significant_data(parsed_data, min_magnitude=6.0):
    significant_only_data = []

    # to check all entries for specified parameters
    for earthquakes in parsed_data:
        if earthquakes["magnitude"] >= min_magnitude:
            significant_only_data.append(earthquakes)

    return significant_only_data

# Code Assembly/ Integration
def main():
    try:
        raw_data = pull_earthquake_data()
        parsed_data = parse_earthquake_data(raw_data)
        filtered_data = filter_significant_data(parsed_data, min_magnitude=6.0)

        if not filtered_data:
            print("No significant earthquakes recorded.")
        else:
            for earthquake in filtered_data:
                print("=" * 40)
                print(f"Earthquake Alert!")
                print(f"Magnitude: {earthquake['magnitude']}")
                print(f"Location: {earthquake['location']}")
                print(f"Time: {earthquake['time']}")
                print(f"Details: {earthquake['url']}")
                print("=" * 40)
    except Exception as e:
        print(f"Error: {e}")

main()