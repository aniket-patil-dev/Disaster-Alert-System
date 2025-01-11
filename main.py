import requests
from dotenv import load_dotenv
import os
import datetime
import json

load_dotenv()

# Retrieves data from Api
def pull_earthquake_data():
    url = os.getenv('earthquake_api_link') # fetches url from env variable
    params = {
        "format": "geojson",
        "starttime": "2025-01-01",
        "minmagnitude": 5.0
    }

    response = requests.get(url=url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to fetch data!")

# Separates unwanted data
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
def filter_significant_data():
    pass

# Code Assembly/ Integration
def main():
    pass
