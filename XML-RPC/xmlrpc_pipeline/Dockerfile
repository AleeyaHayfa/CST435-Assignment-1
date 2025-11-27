FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY server.py .
COPY client.py . 
# Copy client.py too so it can run in the client container
CMD ["python3", "server.py", "8000"]