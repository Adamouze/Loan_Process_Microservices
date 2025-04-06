import grpc
from app.risk_service_proto_client import risk_pb2_grpc, risk_pb2
import os

# Load environment variables
RISK_GRPC_PORT = os.getenv("RISK_GRPC_PORT")

if not RISK_GRPC_PORT:
    raise ValueError("RISK_GRPC_PORT environment variable is not set.")

def evaluate_risk(account_id: int, loan_amount: float):
    with grpc.insecure_channel(f"risk_service:{RISK_GRPC_PORT}") as channel:
        stub = risk_pb2_grpc.RiskServiceStub(channel)
        response = stub.AnalyzeRisk(risk_pb2.RiskRequest(
            account_id=account_id,
            loan_amount=loan_amount
        ))
        return response

