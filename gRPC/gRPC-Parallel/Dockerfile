FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir grpcio grpcio-tools

#generate pb files inside image so they exist

RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. mapreduce.proto

#default command is server on port 50051

CMD ["python","server.py","50051"]
