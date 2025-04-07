from app.services.notifier import send_sms_notification
from app.schema.types import CheckInput

@strawberry.type
class Mutation:
    @strawberry.mutation
    def validate_check(self, check: CheckInput) -> bool:
        # simulate invalid check if amount > 10000
        if check.amount > 10000:
            send_sms_notification(
                phone_number=check.phone_number,
                message="Votre chèque a été refusé. Veuillez contacter votre banque."
            )
            return False
        return True
