from fastapi import APIRouter, Query
from services.check_validation import validate_check_service
from models.check_validation_request import CheckValidationRequest

router = APIRouter(
    prefix="/check_validation",
    tags=["check_validation"]
)

@router.post("/")
def validate_check(request: CheckValidationRequest):
    success = validate_check_service(request.bank_id, request.check_id)
    return {"status": "success" if success else "failed"}
