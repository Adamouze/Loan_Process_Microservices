import requests
import os

CHECK_PORT = os.getenv("CHECK_PORT")
if not CHECK_PORT:
    raise ValueError("CHECK_PORT environment variable is not set.")

url = f"http://check_validation_service:{CHECK_PORT}/check_validation"

def validate_check_service(bank_id: int, check_number: str) -> bool:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    query = """
    query ValidateCheckService($bankId: Int!, $checkNumber: String!) {
        validateCheck(bankId: $bankId, checkNumber: $checkNumber)
    }
    """

    variables = {
        "bankId": bank_id,
        "checkNumber": check_number 
    }

    payload = {
        "query": query,
        "variables": variables
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        return data["data"]["validateCheck"]

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de l'appel au service GraphQL: {e}")
        return False

    except (KeyError, TypeError):
        print("Erreur dans la structure de réponse GraphQL.")
        return False
