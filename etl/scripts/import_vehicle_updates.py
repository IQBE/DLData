'''
    Import the real-time data from the De Lijn API and store it in a database.
'''

import os
import urllib.error
import urllib.parse
import urllib.request
import requests
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from datetime import datetime

load_dotenv()

skey = os.getenv('SKEY', 'unknown_skey')
static_key = os.getenv('STATIC_KEY', 'unknown_static_key')

database_config = {
    'name': os.getenv('DATABASE_NAME', 'unknown_name'),
    'user': os.getenv('DATABASE_USER', 'unknown_user'),
    'password': os.getenv('DATABASE_PASSWORD', 'unknown_password'),
    'host': os.getenv('DATABASE_HOST', 'unknown_host'),
    'port': os.getenv('DATABASE_PORT', 'unknown_port'),
}


unknown_keys = [
    key for key in database_config if database_config[key].startswith('unknown')]
if len(unknown_keys) > 0:
    print(f'ERROR: Unknown environment variables: {", ".join(x for x in unknown_keys)}.')
    exit()

sqlalchemy_url = f'postgresql+psycopg://{database_config["user"]}:{database_config["password"]}@{database_config["host"]}:{database_config["port"]}/{database_config["name"]}'

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
print('Retrieving data from De Lijn API...')
response = requests.get(api_url, headers=headers, params=params)

if response.status_code == 200:
    try:
        data = response.json()
        print('Successfully retrieved data!')
    except Exception as e:
        print('An error occurred:', e)
        print('Response:', response.text)
        exit()
else:
    print('Failed to retrieve data! Status code:', response.status_code)
    print('Response:', response.text)
    exit()


def flatten_data(tu):
    u = tu['tripUpdate']
    t = u['trip']
    result = {
        'trip_id': t['tripId']
    }
    # Incorrect data formats, however allways empty... Skipping for now
    # if 'startDate' in t:
    #     result['trip_start_date'] = t['startDate']
    # if 'scheduleRelationship' in t:
    #     result['trip_schedule_relationship'] = t['scheduleRelationship']
    if 'stopTimeUpdate' in u:
        result['departure_delay'] = u['stopTimeUpdate'][0]['departure']['delay']
        if 'stopId' in u['stopTimeUpdate'][0]:
            result['departure_stop_id'] = u['stopTimeUpdate'][0]['stopId']
        if 'vehicle' in u:
            result['vehicle'] = u['vehicle']['id']
        if 'timestamp' in u:
            result['timestamp'] = datetime.fromtimestamp(u['timestamp'])
    return result


print('Transforming data...', end='')
datalist = [flatten_data(tu) for tu in data['entity']]
tripsdf = pd.DataFrame(datalist)
print('DONE!')

print('Filtering data...', end='')
tripsdf = tripsdf[tripsdf.vehicle.notnull()]
tripsdf = tripsdf.drop_duplicates(subset=['trip_id'], keep='last')
print('DONE!')
print('Number of entries:', len(tripsdf))

# Export data to database
print('Writing data to database:')
engine = create_engine(sqlalchemy_url)
Session = sessionmaker(bind=engine)

print('- Writing to temp database...', end='')
tripsdf.to_sql('temp_table', con=engine,
               if_exists='replace', index=False)
print('DONE!')

upsert_query = '''
INSERT INTO vehicle_updates (trip_id, departure_delay, departure_stop_id, vehicle, timestamp)
SELECT * FROM temp_table
ON CONFLICT (trip_id) DO UPDATE
SET departure_delay = EXCLUDED.departure_delay,
    departure_stop_id = EXCLUDED.departure_stop_id,
    vehicle = EXCLUDED.vehicle,
    timestamp = EXCLUDED.timestamp;
'''
with Session() as session:
    print('- Upserting data...', end='')
    session.execute(text(upsert_query))
    print('DONE!')
    print('- Deleting temp table...', end='')
    session.execute(text('DROP TABLE temp_table'))
    session.commit()
    print('DONE!')

print('Data successfully written to database!')

with engine.connect() as connection:
    res = connection.execute(text('SELECT COUNT(*) FROM vehicle_updates'))
    count = res.scalar()
    print(f'Table "vehicle_updates" now contains {count} rows.')
