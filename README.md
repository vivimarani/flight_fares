## Data Engineering Final Project - Overview

## Business Problem

    * Buying the cheapest fare possible to a round trip


## QPX Express (Flight Fares)  API

[API documentation](https://developers.google.com/qpx-express/)

    API endpoint: https://www.googleapis.com/qpxExpress/v1/trips/search


## Pipeline 

QPX Express -> Kinesis Firehose -> S3 -> Spark -> ML (predict cheapest ticket) -> Some DB --> Flask
Web scraping -> Kinesis Firehose -> S3 -> Spark -> ML (compare ticket price to QPX Express) -> Some DB --> Spyre 
