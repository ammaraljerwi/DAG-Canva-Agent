import requests
from requests.auth import HTTPBasicAuth
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone

from src.database import crud
from src.core.config import settings


def getAccessToken(db: Session, user_id):
    stored_auth = crud.get_auth_token(db, user_id)
    if not stored_auth:
        return None

    expiration = stored_auth.expires_in.replace(tzinfo=timezone.utc)
    time_buffer = timedelta(minutes=10)

    if expiration:
        a_bit_before = expiration - time_buffer
        if datetime.now(timezone.utc) < a_bit_before:
            print("More than 10 mins left")
            return stored_auth.access_token

    refreshed_token = stored_auth.refresh_token
    print(refreshed_token)

    auth = HTTPBasicAuth(settings.CANVA_CLIENT_ID, settings.CANVA_CLIENT_SECRET)
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "refresh_token", "refresh_token": refreshed_token}
    response = requests.post(
        "https://api.canva.com/rest/v1/oauth/token",
        headers=headers,
        data=data,
        auth=auth,
    )

    if not response.ok:
        return None

    refreshed_token = response.json()

    if not refreshed_token:
        return None

    crud.set_auth_token(
        db,
        user_id=user_id,
        access_token=refreshed_token["access_token"],
        refresh_token=refreshed_token["refresh_token"],
        expires_in=datetime.now(timezone.utc)
        + timedelta(seconds=refreshed_token["expires_in"]),
        scopes=refreshed_token["scope"] if refreshed_token["scope"] else None,
        jsonfile=refreshed_token,
    )

    return refreshed_token["access_token"]
