#!/usr/bin/env python

'''
This script is:
1) Spark is "grabbing" files in S3 created from API calls,
2) Parsing JSON file to filter for data we are interested in
3) Loading filtered data into postgres database in 3NF
'''

import json
from os.path import expanduser
import psycopg2
from psycopg2 import IntegrityError, InternalError
import sys
import time
import yaml
from boto.s3.connection import S3Connection
from boto.s3.key import Key

'''
Schema w/ 2 tables
TABLE flights has the following columns:
    tweet_id - bitint - PRIMARY KEY and NOT NULL
    text - character varying
    user_id - bigint
    timestamp_ms - bigint
    created_at - timestamp w/ tz
    lang - character varying
    possibly_sensitive - Boolean

TABLE users has the following columns:
    user_id - bigint - PRIMARY KEY and NOT NULL
    screen_name - character varying
    followers_count - bigint
'''

def get_flights(flights_str):
    '''
    INPUT: JSON string of flights
    OUTPUT: list of length _____ w/ the following values:
            1)
            2)
            3)
            4)
    '''
    try: #write code to pull specific data from the JSON file
         flights = json.loads(flights_str)


    except ValueError:
        pass
def get_fares(flights_str):


def main(credentials, source=sys.stdin):
    '''
    INPUT: None
    OUTPUT: None
        Inserts all flights into postgres using get_flights
    For more on the errors see:
        http://initd.org/psycopg/docs/module.html#exceptions
    '''

    conn = psycopg2.connect(**credentials['rds'])  # connect to postgres
    cur = conn.cursor()  # create a cursor

    total_count = 0

    query_template = 'INSERT INTO ...'



    s3_conn = S3Connection(**credentials['aws'])
    bucket = s3_conn.get_bucket('qpxexpress') #flight jsons bucket


    row_count, total_count = 0, 0
    for key in bucket.list():
        try:
            flight_string = key.get_content_from_string(key.name)
            flight_json = json.loads(flight_string)
        except:
            continue

        try:
            table_1_row = [flight_json['first'], flight_json['second']]
            cur.execute(query_template, table_1_row)
            row_count += 1
        except:
            print("Something bad happened...")
            continue

        if row_count > 99:
            conn.commit()
            row_count = 0


    conn.execute('')
    conn.commit()
    conn.close()
    print('Inserted {} flights'.format(total_count))


if __name__ == '__main__':
    credentials = yaml.load(open(expanduser('~/qpx_express_cred.yml')))
    main(credentials=credentials['rds'])
