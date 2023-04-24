import os
import time
from prometheus_client import start_http_server, CollectorRegistry, Gauge

# Set the port to expose Prometheus metrics on
PROMETHEUS_PORT = 29090

# Create the Prometheus metric to track file read time
registry = CollectorRegistry()
file_read_time = Gauge('file_read_time', 'Time taken to read the file', registry=registry)

# Start the HTTP server to expose Prometheus metrics on the specified port
start_http_server(PROMETHEUS_PORT)

# Set the directory to read files from
DIRECTORY_TO_READ_FROM = 'path/to/directory'

# Continuously read files from the directory
while True:
    for root, dirs, files in os.walk(DIRECTORY_TO_READ_FROM):
        for file in files:
            # Get the full path of the file
            file_path = os.path.join(root, file)
            
            # Read the file and measure the time it takes
            start_time = time.monotonic()
            with open(file_path, 'rb') as f:
                f.read()
            end_time = time.monotonic()

            # Calculate the time taken to read the file and update the Prometheus metric
            file_read_time.set(end_time - start_time)

            # Remove the file once it's been read
            os.remove(file_path)

    # Wait for 5 seconds before checking for new files
    time.sleep(5)
