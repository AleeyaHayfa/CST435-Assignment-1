FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir fastapi uvicorn requests pydantic

# Copy all files (including service folders and client)
COPY . .

# Set PYTHONPATH so services can import common modules if needed
ENV PYTHONPATH="${PYTHONPATH}:/app"

# Default command (overridden in docker-compose)
CMD ["sleep", "infinity"]
