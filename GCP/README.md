# Stock_Market_Real_Time
## Steps

#### SCRIPT GCP_Stock_Market_Real_Time
        - Send data reading from indexProcessed.csv to GCP Pub/Sub
        - name -> GCP_Stock_Market_Real_Time.ipynb 

#### GCP PUB SUB:
###### Details
        - topic -> stock_market_real_time_pub_sub
        - subscription -> stock_market_real_time_pub_sub
        - delivery type -> pull
        - all configuration -> default

#### GCP DATAFLOW WORKBENCH
        - script -> stock_market_real_time_dataflow.py

## Architecture-Diagram
![Architecture-Diagram](Stock-Market-Real-Time-Azure-GCP.jpg)