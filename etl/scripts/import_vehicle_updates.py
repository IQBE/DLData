'''
    Import the real-time data from the De Lijn API and store it in a database.
'''

import os
import urllib.error
import urllib.parse
import urllib.request
import requests
import json
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

skey = os.getenv('SKEY', 'unknown_skey')
static_key = os.getenv('STATIC_KEY', 'unknown_static_key')

database_config = {
    'name': os.getenv('DATABASE_NAME', 'unknown_name'),
    'user': os.getenv('DATABASE_USER','unknown_user'),
    'password': os.getenv('DATABASE_PWD', 'unknown_password'),
    'host': os.getenv('DATABASE_HOST', 'unknown_host'),
    'port': os.getenv('DATABASE_PORT', 'unknown_port'),
}

sqlalchemy_url = f"postgresql+psycopg://{database_config['user']}:{database_config['password']}@{database_config['host']}:{database_config['port']}/{database_config['name']}"

headers = {
    'Ocp-Apim-Subscription-Key': skey,
}

params = urllib.parse.urlencode({
    'canceled': False,
    'delay': False,
    'position': True,
})

api_url = 'https://api.delijn.be/gtfs/v3/realtime?json=true'

# Get data from api
response = requests.get(api_url, headers=headers, params=params)

if response.status_code == 200:
    try:
        data = response.json()
        print('Successfully retrieved data.')
    except Exception as e:
        print('An error occurred:', e)
        print('Response:', response.text)
        exit()
else:
    print('Failed to retrieve data! Status code:', response.status_code)
    print('Response:', response.text)
    print(skey)
    exit()

def flatten_trip_update(tu):
    u = tu['tripUpdate']
    t = u['trip']
    result = {
        'id': tu['id'],
        'tripId': t['tripId']
    }
    if 'startDate' in t:
        result['tripStartDate'] = t['startDate']
    if 'scheduleRelationship' in t:
        result['tripScheduleRelationship'] = t['scheduleRelationship']
    if 'stopTimeUpdate' in u:
        result['departureDelay'] = u['stopTimeUpdate'][0]['departure']['delay']
        if 'stopId' in u['stopTimeUpdate'][0]:
            result['departureStopId'] = u['stopTimeUpdate'][0]['stopId']
        if 'vehicle' in u:
            result['vehicle'] = u['vehicle']['id']
        if 'timestamp' in u:
            result['timestamp'] = u['timestamp']
    result['orig'] = tu
    return result

triplist = [flatten_trip_update(tu) for tu in data['entity']]
tripsdf = pd.DataFrame(triplist)
vehicleUpdates = tripsdf[tripsdf.vehicle.notnull()]
vehicleUpdates.loc[:, 'orig'] = vehicleUpdates['orig'].apply(json.dumps)

# Export data to database
engine = create_engine(sqlalchemy_url)

try:
    vehicleUpdates.to_sql('vehicle_updates', con=engine, if_exists='replace', index=False)
    print("DataFrame successfully written to SQL table.")
except Exception as e:
    print("An error occurred:", e)
    exit()
    
with engine.connect() as connection:
    res = connection.execute(text('SELECT COUNT(*) FROM vehicle_updates'))
    count = res.scalar()
    print(f"Table 'vehicle_updates' contains {count} rows.")