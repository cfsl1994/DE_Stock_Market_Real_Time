# Stock_Market_Real_Time
## Steps

#### AZURE EVENT HUB:
###### Overview
        - Event Hubs Instance -> stock_market_real_time
        - Resource group -> data-engineering
        - Namespace -> data-engineering-event-hub

###### Stream Analytics jobs
        - job name -> stock-market-real-time-capture
        - Input -> Event Hub
                - Event Hub instance Consumer Group -> stock-market-realt-time-capture-cg
                - Serialization -> Json
                - Authentication mode -> Connection String
                - Event Hub shared access key name -> RootManageSharedAccessKey
                - Event Hub shared access key -> YOUR ACCESS KEY

        Output ->  Azure Data Lake Storage Gen2
                - Storage account name -> YOUR DATA STAGE ZONE STORAGE
                - Container -> stock-market-real-time
                - Authentication mode -> Connection String
                - Storage account key -> YOUR STORAGE KEY
                - Serialization -> Parquet
                - Write mode -> Append as results arrive
                - Directory path pattern -> tbl_stock_market_real_time/{date}/{time}/
                - Date pattern -> yyyy-mm-dd
                - Time pattern -> HH
                - All configuration -> Default


#### AZURE DATA LAKE GEN 2
###### General Configuration
        - STORAGE ACCOUNT -> YOUR STAGE ZONE STORAGE ACCOUNT
        - Container -> stock-market-real-time
        - Folder -> tbl_stock_market_real_time 


#### AZURE SINAPSE ANALYTICS
###### 

## Architecture-Diagram
![Architecture-Diagram](Stock-Market-Real-Time-Azure-AZURE.jpg)