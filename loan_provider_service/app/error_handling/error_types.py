class BaseCustomError(Exception):
    HTTP_STATUS_CODE = 505
    default_message = "Internal error"

    def __init__(self, message=None):
        self.message = message or self.default_message
        super().__init__(self.message)

    def __str__(self):
        return self.message

class NotFoundError(BaseCustomError):
    HTTP_STATUS_CODE = 404
    default_message = "Resource not found"

class AlreadyExistsError(BaseCustomError):
    HTTP_STATUS_CODE = 400
    default_message = "Resource already exists"

class InsufficientFundsError(BaseCustomError):
    HTTP_STATUS_CODE = 400
    default_message = "Insufficient funds"

class LoanAmountTooHighError(BaseCustomError):
    HTTP_STATUS_CODE = 400
    default_message = "Loan amount exceeds the maximum limit"
