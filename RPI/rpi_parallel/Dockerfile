# Base image
FROM python:3.11-slim

# Set workdir inside container
WORKDIR /app

# Copy requirements if any (we use requests & fastapi/uvicorn)
RUN pip install --no-cache-dir fastapi uvicorn[standard] requests

# Copy service/client code into container
# We will override WORKDIR in docker-compose for each service/client
COPY . .

# Default command (will be overridden in docker-compose)
CMD ["python", "service_a.py"]
