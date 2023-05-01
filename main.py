import requests
import sqlite3
import datetime
import pytz
import os


endpoint = 'https://api.nasa.gov/neo/rest/v1/feed'
api_key = os.getenv("NASA_API_KEY", "")
table_name = 'neos'


def write_data_to_db(table_name, extracted_data):
    # CREATE TABLE
    conn = sqlite3.connect('{0}.db'.format(table_name))
    c = conn.cursor()
    print("========= CREATING TABLE =========")
    with open("create_neo.sql", "r") as query:
        c.execute(query.read())

    # inserting data from API into table
    print("========= WRITING NEOS TO TABLE =========")
    for l in extracted_data:
        columns = ', '.join(l.keys())
        data = ':' + ', :'.join(l.keys())
        query = 'INSERT INTO neos ({columns}) VALUES ({data})'.format(columns=columns, data=data)
        c.execute(query, l)
    conn.commit()
    conn.close()


def get_neos(end_date, table_name):

    start_date = datetime.date(1982, 12, 10)

    # Using the date difference to create a range for the loop
    extracted_data = []
    for day in range((end_date - start_date).days):
        # running in data batches so as not to overload the endpoint
        batch_start_date = start_date + datetime.timedelta(days=day)
        batch_end_date = batch_start_date + datetime.timedelta(days=6)
        batch_start_date_string = batch_start_date.strftime('%Y-%m-%d')
        batch_end_date_string = batch_end_date.strftime('%Y-%m-%d')
        response = requests.get(endpoint, params={'start_date': batch_start_date_string, 'end_date': batch_end_date_string, 'api_key': api_key})

        # Extract NEO data from API response
        try:
            neo_data = response.json()['near_earth_objects'][batch_start_date_string]

            for neo in neo_data:
                hold = {}
                print("Processing {0}....".format(neo['name']))
                hold["neo_reference_id"] = neo['neo_reference_id'][-4:]
                hold["name"] = neo['name']
                hold["nasa_jpl_url"] = neo['nasa_jpl_url']
                hold["absolute_magnitude_h"] = neo['absolute_magnitude_h']
                hold["estimated_diameter_km_min"] = neo['estimated_diameter']['kilometers']['estimated_diameter_min']
                hold["estimated_diameter_km_max"] = neo['estimated_diameter']['kilometers']['estimated_diameter_max']
                hold["estimated_diameter_meters_min"] = neo['estimated_diameter']['meters']['estimated_diameter_min']
                hold["estimated_diameter_meters_max"] = neo['estimated_diameter']['meters']['estimated_diameter_max']
                hold["estimated_diameter_miles_min"] = neo['estimated_diameter']['miles']['estimated_diameter_min']
                hold["estimated_diameter_miles_max"] = neo['estimated_diameter']['miles']['estimated_diameter_max']
                hold["estimated_diameter_feet_min"] = neo['estimated_diameter']['feet']['estimated_diameter_min']
                hold["estimated_diameter_feet_max"] = neo['estimated_diameter']['feet']['estimated_diameter_max']
                hold["is_potentially_hazardous_asteroid"] = neo['is_potentially_hazardous_asteroid']
                hold["close_approach_date"] = datetime.datetime.utcfromtimestamp(neo['close_approach_data'][0]['epoch_date_close_approach'] / 1000.0).isoformat()
                hold["close_approach_velocity_kms"] = neo['close_approach_data'][0]['relative_velocity']['kilometers_per_second']
                hold["close_approach_velocity_kmh"] = neo['close_approach_data'][0]['relative_velocity']['kilometers_per_hour']
                hold["close_approach_velocity_mph"] = neo['close_approach_data'][0]['relative_velocity']['miles_per_hour']
                hold["miss_distance_astronomical"] = neo['close_approach_data'][0]['miss_distance']['astronomical']
                hold["miss_distance_lunar"] = neo['close_approach_data'][0]['miss_distance']['lunar']
                hold["miss_distance_kilometers"] = neo['close_approach_data'][0]['miss_distance']['kilometers']
                hold["miss_distance_miles"] = neo['close_approach_data'][0]['miss_distance']['miles']
                hold["orbiting_body"] = neo['close_approach_data'][0]['orbiting_body']
                hold["is_sentry_object"] = neo['is_sentry_object']
                extracted_data.append(hold)
        except KeyError:
            continue

    write_data_to_db(table_name, extracted_data)


if __name__ == '__main__':
    end_date = datetime.date.today()
    get_neos(end_date, 'neos')
