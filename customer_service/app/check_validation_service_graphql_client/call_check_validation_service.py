import requests
import os

CHECK_PORT = os.getenv("CHECK_PORT")

if not CHECK_PORT:
    raise ValueError("CHECK_PORT environment variable is not set.")

url = f"http://check_validation_service:{CHECK_PORT}/graphql" 

def validate_check_service(bank_id: int, check_id: int) -> bool:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    query = """
    query ValidateCheckService($bankId: Int!, $checkId: Int!) {
        validate_check(bank_id: $bankId, check_id: $checkId)
    }
    """
    variables = {
        "bankId": bank_id,
        "checkId": check_id
    }
    payload = {
        "query": query,
        "variables": variables
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data["data"]["validate_check"]
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de l'appel au service GraphQL: {e}")
        return False
    except KeyError:
        print("Erreur dans la réponse GraphQL.")
        return False