import os
import random
import time
from datetime import datetime
from prometheus_client import start_http_server, CollectorRegistry, Gauge

# Set the port to expose Prometheus metrics on
PROMETHEUS_PORT = 19090

# Create the Prometheus metric to track file write time
registry = CollectorRegistry()
file_write_time = Gauge('file_write_time', 'Time taken to write the file', registry=registry)

# Create the directory structure to write files to
DIRECTORY_TO_WRITE_TO = 'path/to/directory'

# Create a random file of size 1.4 MB
FILE_SIZE = 1400000
random_data = os.urandom(FILE_SIZE)

# Create a function to write the file and measure the time it takes
def write_file():
    # Create the directory structure based on the current time
    now = datetime.now()
    directory_path = os.path.join(DIRECTORY_TO_WRITE_TO, now.strftime('%Y'), now.strftime('%m'),
                                  now.strftime('%d'), now.strftime('%H'), now.strftime('%M'))
    os.makedirs(directory_path, exist_ok=True)

    # Write the file and measure the time it takes
    start_time = time.monotonic()
    file_path = os.path.join(directory_path, f'{now.strftime("%S")}.dat')
    with open(file_path, 'wb') as f:
        f.write(random_data)
    end_time = time.monotonic()

    # Calculate the time taken to write the file and update the Prometheus metric
    file_write_time.set(end_time - start_time)

# Start the HTTP server to expose Prometheus metrics on the specified port
start_http_server(PROMETHEUS_PORT)

# Write files every minute for 30 minutes
for i in range(30):
    write_file()
    time.sleep(60)

# Sleep for 5 seconds to give the last file a chance to be read
time.sleep(5)
