#!/bin/bash
trap "kill 0" EXIT

echo "--- Starting RPC Pipeline ---"

# Start Service 5
export PORT=8005
export SERVICE_NAME="Service 5"
unset NEXT_HOST
unset NEXT_PORT
python3 service.py &
sleep 0.5

# Start Service 4
export PORT=8004
export SERVICE_NAME="Service 4"
export NEXT_HOST=localhost
export NEXT_PORT=8005
python3 service.py &
sleep 0.5

# Start Service 3
export PORT=8003
export SERVICE_NAME="Service 3"
export NEXT_HOST=localhost
export NEXT_PORT=8004
python3 service.py &
sleep 0.5

# Start Service 2
export PORT=8002
export SERVICE_NAME="Service 2"
export NEXT_HOST=localhost
export NEXT_PORT=8003
python3 service.py &
sleep 0.5

# Start Service 1
export PORT=8001
export SERVICE_NAME="Service 1"
export NEXT_HOST=localhost
export NEXT_PORT=8002
python3 service.py &
sleep 1

# Run Client
export ENTRY_HOST=localhost
export ENTRY_PORT=8001
python3 client.py

wait
