import strawberry

@strawberry.type
class Query:
    @strawberry.field
    def validate_check(self, bank_id: int, check_id: int) -> bool:
        from resolvers.check_validation import validate_check_resolver
        return validate_check_resolver(bank_id, check_id)
