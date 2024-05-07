from datetime import datetime
import io as python_io
import logging
import random
import csv

from apache_beam import (
    DoFn,
    GroupByKey,
    io,
    ParDo,
    Pipeline,
    PTransform,
    WindowInto,
    WithKeys,
)
from apache_beam.options.pipeline_options import PipelineOptions, GoogleCloudOptions, WorkerOptions, StandardOptions
from apache_beam.transforms.window import FixedWindows

class GroupMessagesByFixedWindows(PTransform):
    """A composite transform that groups Pub/Sub messages based on publish time
    and outputs a list of tuples, each containing a message and its publish time."""

    def __init__(self, window_size, num_shards=5):
        self.window_size = int(window_size * 60)  # Convert minutes to seconds
        self.num_shards = num_shards

    def expand(self, pcoll):
        return (
            pcoll
            | "Window into fixed intervals" >> WindowInto(FixedWindows(self.window_size))
            | "Add key" >> WithKeys(lambda _: random.randint(0, self.num_shards - 1))
            | "Group by key" >> GroupByKey()
        )


class WriteToGCS(DoFn):
    def __init__(self, output_path):
        self.output_path = output_path

    def process(self, key_value, window=DoFn.WindowParam):
        ts_format = "%H:%M"
        window_start = window.start.to_utc_datetime().strftime(ts_format)
        window_end = window.end.to_utc_datetime().strftime(ts_format)
        shard_id, batch = key_value
        filename = f"{self.output_path}output-{window_start}-{window_end}-{shard_id}.csv"

        # Use Python's in-memory text stream to leverage csv.writer
        with python_io.StringIO() as string_io:
            writer = csv.writer(string_io)
            headers_written = False
            
            for message_body in batch:
                if isinstance(message_body, bytes):
                    message_body = message_body.decode('utf-8')
                data = json.loads(message_body)
                
                # Rename 'Adj Close' to 'Adj_Close'
                if 'Adj Close' in data:
                    data['Adj_Close'] = data.pop('Adj Close')

                if not headers_written:
                    # Write headers if not yet written
                    headers = list(data.keys())
                    writer.writerow(headers)
                    headers_written = True

                # Write the data row
                writer.writerow(data.values())
            
            # Retrieve the entire CSV content from the StringIO object
            csv_content = string_io.getvalue()
        
        # Write the CSV content to GCS, encoding it to bytes
        with io.gcsio.GcsIO().open(filename=filename, mode="wb") as file:
            file.write(csv_content.encode('utf-8'))
            
        
def run():
    input_subscription = 'projects/PROJECT ID/subscriptions/stock_market_real_time_pub_sub'
    output_path = 'gs://YOUR STAGE ZONE STORAGE GCP/stock_market_real_time/'
    window_size = 1.0  # in minutes
    num_shards = 5

    pipeline_options = PipelineOptions()
    standard_options = pipeline_options.view_as(StandardOptions)
    standard_options.streaming = True  # Properly set streaming mode here

    google_cloud_options = pipeline_options.view_as(GoogleCloudOptions)
    google_cloud_options.region = 'YOUR SUB REGION'
    google_cloud_options.enable_streaming_engine = True
    
    worker_options = pipeline_options.view_as(WorkerOptions)
    worker_options.subnetwork = 'https://www.googleapis.com/compute/v1/projects/PROJECT ID/regions/YOUR SUB REGION/subnetworks/default'
    worker_options.zone = 'YOUR SUB REGION'

    with Pipeline(options=pipeline_options) as pipeline:
        (
            pipeline
            | "Read from Pub/Sub" >> io.ReadFromPubSub(subscription=input_subscription)
            | "Window into" >> GroupMessagesByFixedWindows(window_size, num_shards)
            | "Write to GCS" >> ParDo(WriteToGCS(output_path))
        )

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    run()