import jwt
import time

from pathlib import Path


APP_ID = "4071149"


def generate_app_jwt():
    private_key_path = (
        Path(__file__).resolve().parent.parent
        / "secrets"
        / "copperrabbitai.2026-06-16.private-key.pem"
    )

    with open(private_key_path, "r") as f:
        private_key = f.read()

    payload = {
        "iat": int(time.time()) - 60,
        "exp": int(time.time()) + (10 * 60),
        "iss": APP_ID,
    }

    encoded_jwt = jwt.encode(
        payload,
        private_key,
        algorithm="RS256"
    )

    return encoded_jwt
