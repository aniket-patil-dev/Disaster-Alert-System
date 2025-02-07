import json
import requests
import datetime
import boto3
import os


def pull_earthquake_data():
    url = os.getenv('EARTHQUAKE_API_LINK')  # Fetch URL from environment variables
    params = {
        "format": "geojson",
        "starttime": (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d'),
        "minmagnitude": 5.0
    }
    response = requests.get(url=url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to fetch data!")


def parse_earthquake_data(data):
    parsed_data = []
    for feature in data['features']:
        earthquake = {
            "id": feature['id'],  # Unique earthquake ID
            "magnitude": feature['properties']['mag'],
            "location": feature['properties']['place'],
            "time": datetime.datetime.utcfromtimestamp(feature['properties']['time'] / 1000).strftime(
                '%Y-%m-%d %H:%M:%S'),
            "coordinates": feature['geometry']['coordinates'],
            "url": feature['properties']['url']
        }
        parsed_data.append(earthquake)
    return parsed_data


def filter_new_earthquakes(parsed_data, last_event_id):
    """
    Filters earthquakes that occurred after the last known event.
    """
    new_earthquakes = []
    for earthquake in parsed_data:
        if earthquake['id'] > last_event_id:
            new_earthquakes.append(earthquake)
    return new_earthquakes


def lambda_handler(event, context):
    try:
        # Step 1: Fetch and parse earthquake data
        raw_data = pull_earthquake_data()
        parsed_data = parse_earthquake_data(raw_data)

        # Step 2: Fetch last processed earthquake ID from S3
        s3 = boto3.client('s3')
        bucket_name = os.getenv('S3_BUCKET_NAME')
        key = 'last_event_id.json'

        try:
            response = s3.get_object(Bucket=bucket_name, Key=key)
            last_event_id = json.loads(response['Body'].read())['last_event_id']
        except s3.exceptions.NoSuchKey:
            # No file exists yet, so start with no events processed
            last_event_id = ""

        # Step 3: Filter only new earthquakes
        new_earthquakes = filter_new_earthquakes(parsed_data, last_event_id)

        # Step 4: Update the last processed earthquake ID
        if new_earthquakes:
            new_last_event_id = max(eq['id'] for eq in new_earthquakes)
            s3.put_object(
                Bucket=bucket_name,
                Key=key,
                Body=json.dumps({"last_event_id": new_last_event_id}),
                ContentType="application/json"
            )

        # Step 5: Publish new earthquake alerts to SNS
        sns = boto3.client('sns')
        topic_arn = os.getenv('SNS_TOPIC_ARN')

        for earthquake in new_earthquakes:
            message = (
                f"Earthquake Alert!\n"
                f"Magnitude: {earthquake['magnitude']}\n"
                f"Location: {earthquake['location']}\n"
                f"Time: {earthquake['time']}\n"
                f"Details: {earthquake['url']}"
            )
            sns.publish(TopicArn=topic_arn, Message=message)

        return {
            "statusCode": 200,
            "body": f"Processed {len(new_earthquakes)} new earthquakes."
        }
    except Exception as e:
        return {"statusCode": 500, "body": str(e)}
