FROM python:3.9-slim
WORKDIR /app
RUN pip install jsonrpclib-pelix
COPY . .
CMD ["python", "service.py"]
