from fastapi import FastAPI
from app.routes.check_validation import graphql_app

app = FastAPI()
app.include_router(graphql_app, prefix="/check_validation")
