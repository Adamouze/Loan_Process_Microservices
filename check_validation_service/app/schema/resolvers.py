import strawberry
from schema.types import CheckInput


@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello, World!"

@strawberry.type
class Mutation:
    @strawberry.mutation
    def validate_check(self, check: CheckInput) -> bool:
        is_valid = check.amount <= 1000000
        if not is_valid:
            # Logic for sending notifications
            return False
        return True

schema = strawberry.Schema(query=Query, mutation=Mutation)
