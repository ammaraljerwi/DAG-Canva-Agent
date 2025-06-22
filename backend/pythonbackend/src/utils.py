from jwt import PyJWKClient
import jwt
import requests
from requests.auth import HTTPBasicAuth
import hashlib
import base64
import os

from src.core.config import settings

CANVA_APP_ID = settings.CANVA_APP_ID
CANVA_CLIENT_ID = settings.CANVA_CLIENT_ID
CANVA_CLIENT_SECRET = settings.CANVA_CLIENT_SECRET
REDIRECT_URI = settings.REDIRECT_URI
CANVA_AUTH_URL = "https://www.canva.com/api/oauth/authorize?code_challenge_method=s256&response_type=code&client_id={}&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Fapi%2Fv1%2Fauth%2Foauth%2Fredirect&scope=design:meta:read%20app:read%20design:permission:write%20asset:read%20design:content:read%20design:content:write%20asset:write%20design:permission:read%20app:write&code_challenge={}&state={}"

JWKS_URL = f"https://api.canva.com/rest/v1/apps/{CANVA_APP_ID}/jwks"
jwks_client = PyJWKClient(JWKS_URL)


async def get_access_token_from_code(code_verifier, auth_code):
    auth = HTTPBasicAuth(CANVA_CLIENT_ID, CANVA_CLIENT_SECRET)
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "grant_type": "authorization_code",
        "code_verifier": code_verifier,
        "code": auth_code,
        "redirect_uri": REDIRECT_URI,
    }
    response = requests.post(
        "https://api.canva.com/rest/v1/oauth/token",
        headers=headers,
        data=data,
        auth=auth,
    )
    return response.json()


async def generate_code_verifier(length=64):
    # Allowed chars: [A-Z] / [a-z] / [0-9] / "-" / "." / "_" / "~"
    # We'll use urlsafe_b64encode and strip padding
    verifier = base64.urlsafe_b64encode(os.urandom(length)).decode("utf-8")
    verifier = verifier.rstrip("=")
    # Ensure length is between 43 and 128
    return verifier[:128]


async def generate_code_challenge(verifier):
    digest = hashlib.sha256(verifier.encode("utf-8")).digest()
    challenge = base64.urlsafe_b64encode(digest).decode("utf-8")
    challenge = challenge.rstrip("=")
    return challenge


def get_token_from_header(authorization: str):
    if not authorization:
        return None
    parts = authorization.split()
    if len(parts) == 2 and parts[0].lower() == "bearer":
        return parts[1]
    return None


async def verify_token(token):
    unverified_header = jwt.get_unverified_header(token)
    kid = unverified_header["kid"]
    public_key = jwks_client.get_signing_key_from_jwt(token)
    payload = jwt.decode(
        token,
        public_key,
        algorithms=["RS256"],
        audience=CANVA_APP_ID,
    )
    return payload
