import re

def extract(flight_json):

	#call the private functions here

	tasks = [_get_trips_info, _get_airport_info, _get_city_info,
			_get_aircraft_info, _get_carrier_info]

	keys = ['trips', 'airport', 'city', 'aircraft', 'carrier']

	return {key:task(flight_json) for key, task in zip(keys, tasks)}


def _get_trips_info(flight_json):
	rows = []

	for tripOption in flight_json['trips']['tripOption']:

		try:
			carrier_1 = tripOption['slice'][0]['segment'][0]['leg'][0]['carrier']
			carrier_2 = tripOption['slice'][1]['segment'][0]['leg'][0]['carrier']

			aircraft_1 = tripOption['slice'][0]['segment'][0]['flight']['aircraft']
			aircraft_2 = tripOption['slice'][1]['segment'][0]['flight']['aircraft']

			# should be SFO
			airport_1 = tripOption['slice'][0]['segment'][0]['leg'][0]['origin']

			# should be GRU
			airport_2 = tripOption['slice'][1]['segment'][0]['leg'][0]['origin']

			price_total = float(re.findall("\d+\.\d+", tripOption['saleTotal'])[0])
			duration = sum([int(one_slice['duration']) for one_slice in tripOption['slice']])
			n_segments = sum([len(one_slice['segment']) for one_slice in tripOption['slice']])

			rows.append([duration, price_total, n_segments, airport_1, airport_2,
				aircraft_1, aircraft_2, carrier_1,	carrier_2])
		except:
			print("Extraction failed for requestId: ", flight_json['trips']['requestId'])
			# continue

	return rows

def _get_airport_info(flight_json):
	rows = []

	for item in flight_json['trips']['data']['airport']:
		try:
			rows.append([item['code'], item['city'], item['name']])
		except:
			continue

	return rows

def _get_city_info(flight_json):
	rows = []

	for item in flight_json['trips']['data']['city']:
		try:
			rows.append([item['code'], item['name']])
		except:
			continue

	return rows

def _get_aircraft_info(flight_json):
	rows = []

	for item in flight_json['trips']['data']['aircraft']:
		try:
			rows.append([item['code'], item['name']])
		except:
			continue

	return rows

def _get_carrier_info(flight_json):
	rows = []

	for item in flight_json['trips']['data']['carrier']:
		try:
			rows.append([item['code'], item['name']])
		except:
			continue

	return rows


if __name__ == '__main__':

	import json

	with open("../data/qpx_test_data.json", 'r') as f:
		info = extract(json.loads(f.read()))

	print(info)
