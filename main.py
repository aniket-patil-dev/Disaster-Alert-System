import requests
from dotenv import load_dotenv
import os
import datetime
import json

load_dotenv()

def pull_earthquake_data():
    url = os.getenv('earthquake_api_link')
    params = {
        "format": "geojson",
        "starttime": "2025-01-01",
        "minmagnitude": 5.0
    }

    response = requests.get(url=url, params=params)
    if response.status_code == 200:
        with open(f"earthquake_data-{datetime.datetime.now().date()}-{datetime.datetime.now().time()}.json", "w", encoding='utf-8') as my_file:
            json.dump(response.json(), my_file)
        print("Data Successfully stored")
    else:
        raise Exception("Failed to fetch data!")

pull_earthquake_data()
