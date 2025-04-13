from pydantic import BaseModel
from typing import Optional
import os

CUSTOMER_PORT = os.getenv("CUSTOMER_PORT")

if CUSTOMER_PORT is None:
    raise ValueError("CUSTOMER_PORT environment variable is not set.")

# === Template HTML (dark / navy blue) ===
EMAIL_TEMPLATE: str = """
    <html>
        <head>
            <style>
                body {{
                    background-color: #0d1117;
                    color: #c9d1d9;
                    font-family: Arial, sans-serif;
                    padding: 20px;
                }}
                .container {{
                    background-color: #161b22;
                    padding: 20px;
                    border-radius: 8px;
                    border: 1px solid #30363d;
                }}
                h2 {{
                    color: #58a6ff;
                }}
                a {{
                    color: #58a6ff;
                    text-decoration: none;
                }}
                a:hover {{
                    text-decoration: underline;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Loan Application Status</h2>
                {message}
                <p>Thank you for choosing our services.</p>
                <p>— Loan Services DSI Support Team</p>
            </div>
        </body>
    </html>
"""

class MessageType(BaseModel):
    # === Messages disponibles ===
    Loan_Application_Maximum_Amount_Achieved: str = "Loan Application Rejected: <br><br>Maximum amount achieved."
    Risk_Service_Rejected: str = "Risk Service:<br><br>Application rejected :"
    Risk_Service_Accepted: str = (
        "Risk Service: Application accepted.<br><br>"
        "Next steps:<br><br>"
        f"1) Generate the cashier check: "
        f"<a href='http://localhost:{CUSTOMER_PORT}/docs#/cashier-checks/generate_cashier_check_cashier_checks_generate_post' target='_blank'>Generate Cashier Check</a><br>"
        f"2) Proceed with second part of the loan process: "
        f"<a href='http://localhost:{CUSTOMER_PORT}/docs#/loan-process/loan_process_second_part_loan_process_second_part_post' target='_blank'>Continue Loan Process by submitting the generated cashier check</a>"
        "<br><br>Risk Service details:"
    )
    Check_Validation_Rejected: str = "Check Validation Service: invalid cashier check."
    Loan_Provided: str = (
        "Loan Provider Service:<br><br>Loan provided.<br>Details:"
    )

    @classmethod
    def generate_email(cls, message: str) -> str:
        return EMAIL_TEMPLATE.format(message=f"<p>{message}</p>")

    def get_email_content(self, type_of_message: str, custom_message: str = "") -> str:
        if not hasattr(self, type_of_message):
            raise ValueError(f"Unknown message type: '{type_of_message}'")

        base_message = getattr(self, type_of_message)

        if custom_message:
            base_message += f"<br><br>{custom_message}"

        return self.generate_email(base_message)


class NotificationRequest(BaseModel):
    receiver_address: str
    message: str  # Correspond au nom du champ de MessageType

class NotificationResponse(BaseModel):
    status: bool
    class Config:
        from_attributes = True
