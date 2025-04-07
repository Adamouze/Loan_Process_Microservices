from app.schema.types import CheckInput

def validate_check(check: CheckInput) -> bool:
    if not check.check_id.startswith("CHK"):
        from app.services.notifier import notify_bounced_check
        notify_bounced_check(email="user@example.com")  # À adapter
        return False
    return True
