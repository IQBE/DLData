# Stop editor from formatting on save
# fmt: off
'''
    Import the real-time data from the De Lijn API and store it in a database.
'''

import os
import urllib.error
import urllib.parse
import urllib.request
from typing import Dict, Optional, Iterable
from datetime import datetime
from dataclasses import dataclass, asdict
import requests
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker


@dataclass
class TripEntry:
    '''
    Dataclass to store the trip data.
    '''
    trip_id: str
    departure_delay: Optional[int] = None
    departure_stop_id: Optional[str] = None
    vehicle: Optional[str] = None
    timestamp: Optional[datetime] = None

@dataclass
class DatabaseConfig:
    '''
    Dataclass to store the database configuration.
    '''
    name: str = 'unknown_name'
    user: str = 'unknown_user'
    password: str = 'unknown_password'
    host: str = 'unknown_host'
    port: str = 'unknown_port'
    adapter: str = 'postgresql'


def _parse_data(tu: Dict) -> TripEntry:
    u = tu['tripUpdate']
    t = u['trip']
    trip_id = t['tripId']
    result = TripEntry(trip_id=trip_id)
    if 'stopTimeUpdate' in u:
        result.departure_delay = u['stopTimeUpdate'][0]['departure']['delay']
        if 'stopId' in u['stopTimeUpdate'][0]:
            result.departure_stop_id = u['stopTimeUpdate'][0]['stopId']
        if 'vehicle' in u:
            result.vehicle = u['vehicle']['id']
        if 'timestamp' in u:
            result.timestamp = datetime.fromtimestamp(u['timestamp'])
    return result

def _retrieve_data(api_url: str, headers, params) -> Dict:
    response = requests.get(api_url, headers=headers, params=params)
    if response.status_code == 200:
        response.raise_for_status()
        return response.json()
    else:
        print('Failed to retrieve data! Status code:', response.status_code)
        print('Response:', response.text)
        raise Exception('Failed to retrieve data!')

def get_trip_data(api_key: str) -> Iterable[TripEntry]:
    '''
    Retrieve the real-time data from the De Lijn API.
    '''
    api_url = 'https://api.delijn.be/gtfs/v3/realtime?json=true'

    headers = {
        'Ocp-Apim-Subscription-Key': api_key,
    }

    params = urllib.parse.urlencode({
        'canceled': False,
        'delay': False,
        'position': True,
    })

    print('Retrieving data from De Lijn API...')
    data_raw = _retrieve_data(api_url, headers, params)
    for row in data_raw['entity']:
        yield _parse_data(row)

# Get data from api
def persist_trips(engine: Engine, data: Iterable[TripEntry]) -> None:
    '''
    Transform the data and write it to the database.
    '''
    tripsdf = pd.DataFrame([asdict(x) for x in data])

    print('Filtering data...', end='')
    tripsdf = tripsdf[tripsdf.vehicle.notnull()]
    tripsdf = tripsdf.drop_duplicates(subset=['trip_id'], keep='last')
    print('DONE!')
    print('Number of entries:', len(tripsdf))

    # Export data to database
    print('Writing data to database:')
    Session = sessionmaker(bind=engine)

    print('- Creating temp table...', end='')
    with Session() as session:
        session.execute(text('CREATE TEMP TABLE temp_table (LIKE vehicle_updates INCLUDING ALL)'))
        session.commit()
    print('DONE!')

    print('- Writing to temp database...', end='')
    tripsdf.to_sql('temp_table', con=engine, if_exists='append', index=False)
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

def get_engine(database_config: DatabaseConfig) -> Engine:
    '''
    Create an engine for database connection.
    '''
    sqlalchemy_url = f'{database_config.adapter}://{database_config.user}:{database_config.password}@{database_config.host}:{database_config.port}/{database_config.name}'
    engine = create_engine(sqlalchemy_url)
    return engine

def count_rows(engine: Engine) -> int:
    '''
    Count the rows in the vehicle_updates table.
    '''
    with engine.connect() as connection:
        res = connection.execute(text('SELECT COUNT(*) FROM vehicle_updates'))
        count = res.scalar()
        connection.close()
    return count

def get_skey() -> str:
    '''
    Get the subscription key from the environment variables.
    '''
    load_dotenv()

    skey = os.getenv('SKEY', 'unknown_skey')

    if skey.startswith('unknown'):
        raise Exception('ERROR: Unknown environment variable: SKEY.')

    return skey

def get_database_config() -> DatabaseConfig:
    '''
    Get the database configuration from the environment variables.
    '''
    database_config = DatabaseConfig(
        name=os.getenv('DATABASE_NAME', 'unknown_name'),
        user=os.getenv('DATABASE_USER', 'unknown_user'),
        password=os.getenv('DATABASE_PASSWORD', 'unknown_password'),
        host=os.getenv('DATABASE_HOST', 'unknown_host'),
        port=os.getenv('DATABASE_PORT', 'unknown_port'),
        adapter=os.getenv('DATABASE_ADAPTER', 'postgresql'),
    )

    unknown_keys = [key for key in asdict(database_config).values() if key.startswith('unknown')]
    if len(unknown_keys) > 0:
        raise Exception(f'ERROR: Unknown environment variables: {", ".join(x for x in unknown_keys)}.')

    return database_config

if __name__ == '__main__':
    skey = get_skey()
    database_config = get_database_config()
    engine = get_engine(database_config)

    data = get_trip_data(skey)
    persist_trips(engine, data)
    print(f'Table "vehicle_updates" now contains {count_rows(engine)} rows.')
