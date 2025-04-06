# Dockerfile
FROM python:3.9

WORKDIR /app

# Copying the requirements file first to leverage Docker cache
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code to the container
COPY . .

RUN python -m grpc_tools.protoc \
    -Iapp/risk_service_proto_client \
    --python_out=app/risk_service_proto_client \
    --grpc_python_out=app/risk_service_proto_client \
    app/risk_service_proto_client/risk.proto

RUN sed -i 's/^import risk_pb2/from app.risk_service_proto_client import risk_pb2/' app/risk_service_proto_client/risk_pb2_grpc.py

CMD ["python", "-m", "app.main"]