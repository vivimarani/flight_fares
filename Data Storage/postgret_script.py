#!/usr/bin/env python

'''
This script grabs data from file in S3 and loads into Postgres
'''

import json
from os.path import expanduser
import psycopg2
from psycopg2 import IntegrityError, InternalError
import sys
import time
import yaml

credentials = yaml.load(open(expanduser('~/qpx_express_cred.yml')))

'''
TABLE flights has the following columns:
    _______ - bitint - PRIMARY KEY and NOT NULL
    _______ - character varying - PRIMARY KEY and NOT NULL
    _______  - bigint
    _______  - bigint
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

def main(credentials, source=sys.stdin):
    '''
    INPUT: None
    OUTPUT: None
        Inserts all flights into postgres using `get_flights`
    For more on the errors see:
        http://initd.org/psycopg/docs/module.html#exceptions
    '''

    conn = psycopg2.connect(**credentials['rds'])  # connect to postgres
    cur = conn.cursor()  # create a cursor
    row_count, total_count = 0, 0
    for flights_str in source:
        if ... :
            row_count += 1
            row = get_flights(flights_str)
            try:
#               cur.execute("INSERT INTO flights VALUES")
#           except:
#               pass
        if row_count > 99:
            conn.commit()
            row_count = 0



    conn.commit()
    conn.close()
    print('Inserted {} flights'.format(total_count))

if __name__ == '__main__':
    credentials = yaml.load(open(expanduser('~/.ssh/postgres.yml')))
    main(credentials=credentials['rds'])
