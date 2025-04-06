import grpc
from concurrent import futures
from app.service.risk_service import RiskService
from app.proto import risk_pb2_grpc
import os

RISK_GRPC_PORT = os.getenv("RISK_GRPC_PORT")

if not RISK_GRPC_PORT:
    raise ValueError("RISK_GRPC_PORT environment variable is not set.")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    risk_pb2_grpc.add_RiskServiceServicer_to_server(RiskService(), server)

    server.add_insecure_port(f'[::]:{RISK_GRPC_PORT}')
    print(f"✅ Risk Service gRPC server running on port {RISK_GRPC_PORT}")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
