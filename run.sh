#!/bin/bash

MODE=$1

if [ "$MODE" == "docker" ]; then
    echo "--- Running in DOCKER Mode ---"
    # Build and start containers
    docker-compose up -d --build
    echo "Waiting for workers to initialize..."
    sleep 2
    # Run client inside the Docker network
    docker-compose exec client python client.py
    # Shutdown
    # docker-compose down

elif [ "$MODE" == "local" ]; then
    echo "--- Running in LOCAL Mode ---"
    # Start 5 workers in the background
    python3 server.py 8001 & PID1=$!
    python3 server.py 8002 & PID2=$!
    python3 server.py 8003 & PID3=$!
    python3 server.py 8004 & PID4=$!
    python3 server.py 8005 & PID5=$!
    
    echo "Workers started (PIDs: $PID1 $PID2 $PID3 $PID4 $PID5)"
    sleep 1
    
    # Run client
    export MODE=LOCAL
    python3 client.py
    
    # Kill workers after client finishes
    kill $PID1 $PID2 $PID3 $PID4 $PID5

else
    echo "Usage: ./run.sh [local | docker]"
fi
