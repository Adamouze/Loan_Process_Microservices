from app.schema.types import CheckInput
from app.services.notifier import send_sms_notification
import strawberry

@strawberry.type
class Mutation:
    @strawberry.mutation
    def validate_check(self, check: CheckInput) -> bool:
        # Validation logic (exemple : refus si montant > 1M)
        is_valid = check.amount <= 1000000
        
        if not is_valid:
            message = (
                f"Bonjour {check.full_name}, "
                "votre chèque a été refusé. Veuillez contacter votre banque."
            )
            send_sms_notification(check.phone_number, message)
        
        return is_valid
