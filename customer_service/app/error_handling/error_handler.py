from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.error_handling.error_types import BaseCustomError
from sqlalchemy.exc import SQLAlchemyError

def register_error_handlers(app: FastAPI):

    @app.exception_handler(BaseCustomError)
    async def base_custom_error_handler(request: Request, exc: BaseCustomError):
        return JSONResponse(
            status_code=exc.HTTP_STATUS_CODE,
            content={"detail": exc.message}
        )

    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
        return JSONResponse(
            status_code=500,
            content={"detail": str(exc)}
        )