import os
import time
import requests

IN_DOCKER = os.environ.get("IN_DOCKER", "0") == "1"

def post_with_retry(url, payload, retries=10, delay=0.5):
    """Post payload to URL with retries if running inside Docker."""
    if not IN_DOCKER:
        resp = requests.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()
    
    for i in range(retries):
        try:
            resp = requests.post(url, json=payload)
            resp.raise_for_status()
            return resp.json()
        except requests.ConnectionError:
            print(f"[Retry {i+1}/{retries}] Connection failed to {url}, waiting {delay}s...")
            time.sleep(delay)
    raise Exception(f"Failed to connect to {url} after {retries} retries")
