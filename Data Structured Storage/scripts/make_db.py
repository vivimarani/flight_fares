import yaml
import psycopg2
from functools import reduce
from os.path import expanduser

'''Run this module when using a freshly created DB'''

def make_tables(credentials):
	'''Builds the tables needed'''

	try:
		print("Connecting...")
		print(credentials['rds'])
		conn = psycopg2.connect(**credentials['rds'])
		cur = conn.cursor()
		print("Connection Established")
	except:
		print("Error Establishing Connection (bad credentials?)")
		return False


	results = []
	for i, task in enumerate([_make_trips_table, _make_airport_table, _make_city_table,
					_make_aircraft_table, _make_carrier_table]):
		print("Task {} starting...".format(i))
		results.append(task(cur))

	result = reduce(lambda x, y: x and y, results)

	if result:
		print("Finished Creating Tables. Exiting...")
		conn.commit()
		return True
	else:
		print("Finished Tasks with Errors. Exiting...")
		return False


def _make_trips_table(cur):
	query = """CREATE TABLE IF NOT EXISTS trips (id SERIAL PRIMARY KEY, duration INT,
				price MONEY, n_segments INT,
				origin_airport varchar(20), dest_airport varchar(20),
				origin_aircraft varchar(20), dest_aircraft varchar(20),
				origin_carrier varchar(20), dest_carrier varchar(20));"""
	try:
		cur.execute(query)
		return True
	except:
		print("An error occurred while making airport table")
		return False

def _make_airport_table(cur):
	query  = "CREATE TABLE IF NOT EXISTs airport (code varchar(20) PRIMARY KEY, city varchar(20) NOT NULL, name varchar(100) NOT NULL)"
	try:
		cur.execute(query)
		return True
	except:
		print("An error occurred while making airport table")
		return False

def _make_city_table(cur):
	query  = "CREATE TABLE IF NOT EXISTs city (code varchar(20) PRIMARY KEY, name varchar(100) NOT NULL)"
	try:
		cur.execute(query)
		return True
	except:
		print("An error occurred while making city table")
		return False

def _make_aircraft_table(cur):
	query  = "CREATE TABLE IF NOT EXISTs aircraft (code varchar(20) PRIMARY KEY,  name varchar(100) NOT NULL)"
	try:
		cur.execute(query)
		return True
	except:
		print("An error occurred while making aircraft table")
		return False

def _make_carrier_table(cur):
	query  = "CREATE TABLE IF NOT EXISTs carrier (code varchar(20) PRIMARY KEY,  name varchar(100) NOT NULL)"
	try:
		cur.execute(query)
		return True
	except:
		print("An error occurred while making carrier table")
		return False


if __name__ == "__main__":
	credentials = yaml.load(open(expanduser('~/.ssh/qpx_express_cred.yml')))
	make_tables(credentials)
