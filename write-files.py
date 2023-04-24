import os
import shutil
import random
import time
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

# Set the Prometheus gateway address and job name
PROMETHEUS_GATEWAY = 'http://localhost:9091'
JOB_NAME = 'file_copy_metrics'

# Create the Prometheus metric to track file copy time
registry = CollectorRegistry()
file_copy_time = Gauge('file_copy_time', 'Time taken to copy the file', registry=registry)

# Set the directory to create files in
DIRECTORY_TO_CREATE_IN = 'path/to/directory'

# Generate a random 1.4 MB file to copy every minute for 30 minutes
for i in range(30):
    # Create the directory and subdirectories in yyyy/mm/dd/hh/mm format
    now = time.localtime()
    dir_name = f'{now.tm_year}/{now.tm_mon:02d}/{now.tm_mday:02d}/{now.tm_hour:02d}/{now.tm_min:02d}'
    os.makedirs(os.path.join(DIRECTORY_TO_CREATE_IN, dir_name), exist_ok=True)
    
    # Generate a random 1.4 MB file to copy
    filename = 'random_file.bin'
    with open(filename, 'wb') as f:
        f.write(os.urandom(1400000))
        
    # Copy the file to the directory and measure the time it takes
    start_time = time.monotonic()
    shutil.copy(filename, os.path.join(DIRECTORY_TO_CREATE_IN, dir_name))
    end_time = time.monotonic()

    # Calculate the time taken to copy the file and update the Prometheus metric
    file_copy_time.set(end_time - start_time)

    # Push the Prometheus metric to the gateway
    push_to_gateway(PROMETHEUS_GATEWAY, job=JOB_NAME, registry=registry)

    # Clean up the random file
    os.remove(filename)
    
    # Wait for 1 minute before generating the next file
    time.sleep(60)
