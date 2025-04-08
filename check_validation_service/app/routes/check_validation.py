import strawberry
from strawberry.fastapi import GraphQLRouter
from app.schema.types import CheckInput
from app.services.notifier import notify_bounced_check

@strawberry.type
class Mutation:
    @strawberry.mutation
    def validate_check(self, check: CheckInput) -> bool:
        if not check.check_id.startswith("CHK"):
            notify_bounced_check(phone=check.phone_number, message="Check bounced")
            return False
        return True

schema = strawberry.Schema(mutation=Mutation)
graphql_app = GraphQLRouter(schema)
