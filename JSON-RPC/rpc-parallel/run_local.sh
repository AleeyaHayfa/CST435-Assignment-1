#!/bin/bash
trap "kill 0" EXIT

echo "--- Starting MapReduce Cluster (5 Services) ---"

export SERVICE_NAME="Service 1"
export PORT=8001
python3 service.py &

export SERVICE_NAME="Service 2"
export PORT=8002
python3 service.py &

export SERVICE_NAME="Service 3"
export PORT=8003
python3 service.py &

export SERVICE_NAME="Service 4"
export PORT=8004
python3 service.py &

export SERVICE_NAME="Service 5"
export PORT=8005
python3 service.py &

sleep 2
echo "--- Services Started. Running Client ---"

# Point to all 5 local ports
export WORKER_NODES="localhost:8001,localhost:8002,localhost:8003,localhost:8004,localhost:8005"
python3 client.py

wait
