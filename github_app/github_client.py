import requests

from .auth import generate_app_jwt


APP_ID = "4071149"
INSTALLATION_ID = "140735937"


def get_installation_token():
    jwt_token = generate_app_jwt()

    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/vnd.github+json",
    }

    response = requests.post(
        f"https://api.github.com/app/installations/{INSTALLATION_ID}/access_tokens",
        headers=headers,
    )

    print("Status:", response.status_code)

    print(response.json())

    return response.json()