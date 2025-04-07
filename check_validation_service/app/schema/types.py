import strawberry

@strawberry.input
class CheckInput:
    full_name: str
    bank_name: str
    issue_date: str
    check_id: str
    amount: float
    phone_number: str  # nécessaire pour notifier
