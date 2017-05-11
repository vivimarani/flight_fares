#!/usr/bin/env python

import json
import requests
import boto3
import os


def kin(boto_client,data):
    response_dump = json.dumps(data) + '\n'
    client.put_record(DeliveryStreamName='qpxexpress', Record={'Data': response_dump})

if __name__ == '__main__':

# list of days to travel =
#"2017-07-01","2017-07-02","2017-07-03","2017-07-04","2017-07-05","2017-07-06"
#"2017-07-07","2017-07-08","2017-07-09","2017-07-10","2017-07-11","2017-07-12","2017-07-13",
#"2017-07-14","2017-07-15","2017-07-16","2017-07-17", "2017-07-18","2017-07-19",
# "2017-07-20","2017-07-21","2017-07-22","2017-07-23","2017-07-24","2017-07-25","2017-07-26",
# "2017-07-27",2017-07-28","2017-07-29","2017-07-30","2017-07-31"}

    api_key = "-----------------------py4eg"
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
