import threading, subprocess, time

ports = [50051, 50052, 50053, 50054, 50055]

def run_server(i, port):
        subprocess.run(["python3", "server.py", str(i), str(port)])

print("starting servers...")
for i, port in enumerate(ports, start=1):
        t = threading.Thread(target=run_server, args=(i, port), daemon=True)
        t.start()
        time.sleep(0.1)

time.sleep(1.0)
print("Running Client....\n")
subprocess.run(["python3", "client.py"])
