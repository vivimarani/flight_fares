#!/usr/bin/env python

import json
import requests
import boto3
import os


def kin(boto_client,data):
    response_dump = json.dumps(data) + '\n'
    client.put_record(DeliveryStreamName='qpxexpress', Record={'Data': response_dump})

if __name__ == '__main__':

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
    airline = json.loads(response.content.decode('utf-8'))
    print(airline)
    client = boto3.client('firehose', region_name='us-east-1')
    kin(client,airline)
