import subprocess
import time
import threading
import os

PORTS = [50051, 50052, 50053, 50054, 50055]

def run_server(port):
        subprocess.run(["python3", "server.py", str(port)])

def run_client():
        time.sleep(5)
        subprocess.run(["python3", "client.py"])

if __name__ == "__main__":

        for port in PORTS:
                t = threading.Thread(target=run_server, args=(port,))
                t.daemon = True
                t.start()
                print(f"started server on port {port}")

        run_client()

        while True:
                time.sleep(1)
