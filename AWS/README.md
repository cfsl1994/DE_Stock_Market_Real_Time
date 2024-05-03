# Stock_Market_Real_Time
## Steps

#### SCRIPT Aws_Stock_Market_Real_Time
        - Send data reading from indexProcessed.csv to Azure EventHub
        - name -> Aws_Stock_Market_Real_Time.ipynb 

#### AWS KINESIS:
###### Configuration
        - name -> stock_market_real_time_kinesis_data_stream
        - capacity mode -> On-demand
        - all conifiguration -> default

#### AWS GLUE
###### DATA SOURCE PROPERTIES
        - name -> kinesis stream
        - amazon kinesis source -> stream details
        - location of data stream -> stream is located in my account
        - region -> us-east-2
        - stream name -> stock_market_real_time_kinesis_data_stream
        - data format -> json
        - all conifiguration -> default

###### DATA TARGET PROPERTIES
        - name -> amazon s3
        - node parents -> amazon kinesis
        - format -> parquet
        - compression type -> snappy
        - s3 target location -> YOUR STAGE ZONE BUCKET
        - all conifiguration -> default

#### AWS S3
###### BUCKET
        - bucket -> YOUR STAGE ZONE BUCKET
        - sub directory -> stock_market_real_time

#### AWS GLUE CRAWLER
###### PROPERTIES
        - name -> stock_market_real_time_crawler
        - iam role -> YOUR IAM ROLE
        - database -> stock-market-real-time-db
        - table prefix -> tbl_

###### DATA SOURCE
        - type -> s3
        - data source -> s3://YOUR STAGE ZONE BUCKET/stock-market-real-time
        - parameters -> recrawl all

#### AWS GLUE CATALOG
        - database -> stock-market-real-time-db

#### AWS REDSHIFT SERVERLESS
        - Namespace -> stock-market-real-time-namespace
        - Workgroup -> stock-market-real-time-workgroup

###### Query Editor v2
        - Serverless -> stock-market-real-time-workgroup
        - data catalog ->  awsdatacatalog (Create using AWS Glue Data Catalog)
        - database named -> stock-market-real-time-db
        - tables -> tbl_stock_market_reak_time


## Architecture-Diagram
![Architecture-Diagram](Stock-Market-Real-Time-Azure-AWS.jpg)