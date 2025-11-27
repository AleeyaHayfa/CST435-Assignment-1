import os

def get_target(service_name, default_port):
    if os.getenv("DOCKER_MODE") == "1":
        return f"http://{service_name}:{default_port}"
    else:
        return f"http://localhost:{default_port}"
