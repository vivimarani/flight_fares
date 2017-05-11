#!/usr/bin/env python

# use key.lastmodified to implement CRON job

import json
import yaml
from os.path import expanduser
import psycopg2
from psycopg2 import IntegrityError, InternalError
from boto.s3.connection import S3Connection
from pyspark import SparkContext
import qpx_extractor as Extractor


def update_all_partitions(source):
	'''source is a partition of a RDD'''
	credentials = yaml.load(open(expanduser('../qpx_express_cred.yml')))
	conn, cur = connect_DB(credentials)

	if not source:
		print("Empty partition? Exiting...")
		return

	for i, row in enumerate(source):
		try:
			flight_json = json.loads(row)

			data = Extractor.extract(flight_json)
			_update_trips(conn, cur, data['trips'])
			_update_airport(conn, cur, data['airport'])
			_update_city(conn, cur, data['city'])
			_update_aircraft(conn, cur, data['aircraft'])
			_update_carrier(conn, cur, data['carrier'])
		except:
			continue

		if i % 100 == 0:
			print("Batch {} Complete".format(i%100))

	conn.commit()


def connect_DB(credentials):

	try:
		conn = psycopg2.connect(**credentials['rds'])
		cur = conn.cursor()
		print("Connection Established")
	except:
		print("Error Establishing Connection")
		return None, None

	return conn, cur


def connect_S3(credentials):

	try:
		s3_conn = S3Connection(credentials['aws']['access_key_id'], credentials['aws']['Secret_access_key'])
		bucket = s3_conn.get_bucket('qpxexpress') #flight jsons bucket
		print("S3 Connection Established")
	except:
		print("Error Establishing S3 Connection")
		return None, None

	return s3_conn, bucket


def update_all(credentials):
	''' Takes all data from S3, extracts relevant info, and places in PSQL'''

	conn, cur = connect_DB(credentials)
	s3_conn, bucket = connect_S3(credentials)


	for i, key in enumerate(bucket.list()):

		print(i)

		try:
			flight_string = key.get_contents_as_string().decode('utf-8')
			flight_json = json.loads(flight_string)

			data = Extractor.extract(flight_json)
			_update_trips(conn, cur, data['trips'])
			_update_airport(conn, cur, data['airport'])
			_update_city(conn, cur, data['city'])
			_update_aircraft(conn, cur, data['aircraft'])
			_update_carrier(conn, cur, data['carrier'])
		except:
			continue

		if i % 100 == 0:
			print("Batch {} Complete".format(i%100))

	conn.commit()


def local_test(credentials):

	conn, cur = connect_DB(credentials)

	flight_json = json.loads(open('../data/qpxexpress-1-2017-04-15-06-11-05-2e4631ad-e942-495c-a4aa-ad66cd66e48d', 'r').read())

	data = Extractor.extract(flight_json)

	results = [_update_trips(conn, cur, data['trips']),
			_update_airport(conn, cur, data['airport']),
			_update_city(conn, cur, data['city']),
			_update_aircraft(conn, cur, data['aircraft']),
			_update_carrier(conn, cur, data['carrier'])]

	if all(results):
		print("Test Passed. Exiting...")
	else:
		print("Test Failed. Exiting...")

	conn.commit()


def _update_trips(conn, cur, rows):

	query = """INSERT INTO trips (duration, price, n_segments, origin_airport,
		dest_airport, origin_aircraft, dest_aircraft,
		origin_carrier, dest_carrier) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"""


	for row in rows:
		try:
			cur.execute(query, row)
			conn.commit()
		except (InternalError, IntegrityError):
			conn.rollback()
			print("_update_trip failed for: ", row)
			continue


	return True

def _update_airport(conn, cur, rows):

	query = "INSERT INTO airport (code, city, name) VALUES (%s, %s, %s);"

	for row in rows:
		try:
			cur.execute(query, row)
			conn.commit()
		except (InternalError, IntegrityError):
			conn.rollback()
			print("_update_airport failed for: ", row)
			continue

	return True

def _update_city(conn, cur, rows):

	query = "INSERT INTO city (code, name) VALUES (%s, %s);"

	for row in rows:
		try:
			cur.execute(query, row)
			conn.commit()
		except (InternalError, IntegrityError):
			conn.rollback()
			print("_update_city failed for: ", row)
			continue

	return True

def _update_aircraft(conn, cur, rows):

	query = "INSERT INTO aircraft (code, name) VALUES (%s, %s);"

	for row in rows:
		try:
			cur.execute(query, row)
			conn.commit()
		except (InternalError, IntegrityError):
			conn.rollback()
			print("_update_aircraft failed for: ", row)
			continue

	return True

def _update_carrier(conn, cur, rows):

	query = "INSERT INTO carrier (code, name) VALUES (%s, %s);"

	for row in rows:
		try:
			cur.execute(query, row)
			conn.commit()
		except (InternalError, IntegrityError):
			conn.rollback()
			print("_update_carrier failed for: ", row)
			continue

	return True


if __name__ == "__main__":
	# credentials = yaml.load(open(expanduser('../qpx_express_cred.yml')))
	# flight_json = json.loads(open('../data/qpx_test_data.json', 'r').read())
	# local_test(credentials)
	# update_all(credentials)
	sc = SparkContext()
	rdd = sc.textFile('s3a://qpxexpress/*/*/*')
	rdd.foreachPartition(update_all_partitions)
