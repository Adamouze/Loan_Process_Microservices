from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
import strawberry
import uvicorn
from schema.schema import Query
import os

CHECK_PORT = int(os.getenv("CHECK_PORT"))

if not CHECK_PORT or CHECK_PORT <= 0:
    raise ValueError("CHECK_PORT environment variable not set.")

# Init schema et router GraphQL
schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema)

# FastAPI app initialization
app = FastAPI()
app.include_router(graphql_app, prefix="/check_validation")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=CHECK_PORT)