from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from schema.resolvers import schema

app = FastAPI()

graphql_app = GraphQLRouter(schema)

app.include_router(graphql_app, prefix="/check_validation")
