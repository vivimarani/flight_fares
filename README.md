## Data Engineering Final Project - Overview

## Business Problem

    * Buying the cheapest fare possible to a round trip

# The "5Ss"
    * Streaming
    * Storing
    * Structuring
    * Synthesizing
    * Show

## Pipeline 

<img src="my_dag.png">



# Streaming

### Streaming data from REST API 
**QPX Express API (Flight Fares) **

    * Send HTTP POST request to API endpoint: https://www.googleapis.com/qpxExpress/v1/trips/search
    * more info at Final-Project-QPX-Express-API.ipynb
    
## Kinesis
    * Setup Kinesis firehose on AWS using boto3 to pull data from API
    * Specify the bucket that I want to direct the firehose to in S3
    * Use the cronjob to run test_api.py every 30 minutes


# Storing
    * Data lake on S3

# Structuring  

### Apache Parquet
    * Read raw data from s3
    * Create Spark dataFrames in 3 nf
    * Store them in s3 as parquet for backup

### RDS - PostgreSQL

    * Create 2 tables (International vs National) via pgAdmin
    * Read data into each table using a spark script

# Synthesizing
    * ML Lib
    * Scikit-Learn

# Show
    * Run Flask on a new EC2 instance, use the final_flask.py.
    * Run Spyre on a new EC2 instance, use the final_spyre.py.


-------
 
# 8 properties for Big Data systems :

## Robustness and fault Tolerance
Since all the systems used belong to AWS. All systems used for the project neatly integrates with one another, with good Robustness.

All the raw data required is stored in s3. Incase some system fails, the data can still be used to recompute the desired results.


## Low latency reads and updates
Using kanesis to store the data in s3 and reading this data off of s3 shouldn't take long.

When it comes to the analysis of historical surge data, Latency is not very important. But, using spark cuts down thelatency on general by avoiding unnecessary disk i/o.

## Scalability
I do not have a high volume of data, but in case that increases, S3 is good enough to hold huge amount of data.

## Generalization
This architecture can be reused for a lot of applications. Especially for using another API or webscraping.

## Extensibility
Apart from the sysytems that store the raw data, any of the system can be replaced with a better ones if there are any available, or may be for a different application, using the same data.

## Ad hoc queries
PostgreSQL will be used to do ad hoc queries.


## Minimal maintainance
As all the components are maintained AWS, there is very less to worry about interms of maintainance.

When it comes to scale, the postgresql can be of a problem. This an be replaced with an appropriate rdbms system

## Debuggability
I will be having some checkpoints at some stages in my pipeline, to make sure that everything is running as planned. These checkpoints can be like a mail to notify myself the amount/count of data that I have collected.If the RDBMS crashes, there will be a parquet on s3 to fall back on.
