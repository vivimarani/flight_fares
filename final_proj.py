#!/usr/bin/env python

import json
import requests
import pprint

api_key = "AIzaSyBxO2z1DjQ99WERQCHGApEoi-ccxLpy4eg"
url = "https://www.googleapis.com/qpxExpress/v1/trips/search?key=" + api_key
headers = {'content-type': 'application/json'}
params = {
  "request": {
    "slice": [
      {
        "origin": "SFO",
        "destination": "GRU",
        "date": "2017-07-22"
      },
      {
        "origin": "GRU",
        "destination": "SFO",
        "date": "2017-08-13"
      }
    ],
    "passengers": {
        "adultCount": 1,
        "infantInLapCount": 0,
        "infantInSeatCount": 0,
        "childCount": 0,
        "seniorCount": 0
    },
    "solutions": 10,
    "refundable": False
  }
}

response = requests.post(url, data=json.dumps(params), headers=headers)
data = response.json()
