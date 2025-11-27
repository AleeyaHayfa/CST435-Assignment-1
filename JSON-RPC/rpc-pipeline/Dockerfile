FROM python:3.9-slim

WORKDIR /app

# Install the JSON-RPC library
RUN pip install jsonrpclib-pelix

COPY . .

CMD ["python", "service.py"]
