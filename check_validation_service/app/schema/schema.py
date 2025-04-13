import strawberry
from resolvers.check_validation import validate_check_resolver

@strawberry.type
class Query:
    @strawberry.field
    def validate_check(self, bank_id: int, check_number: str) -> bool:
        return validate_check_resolver(bank_id, check_number)
