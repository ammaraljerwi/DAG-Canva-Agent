from fastapi import APIRouter, Response, Cookie
from fastapi import Request, Header, HTTPException, Query, Depends
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from typing import Annotated, Union

from src.core.security import getAccessToken
from src.database import crud
from src.database.database import get_db
from src.schemas import user
from src.utils import (
    generate_code_verifier,
    generate_code_challenge,
    get_access_token_from_code,
    get_token_from_header,
    verify_token,
)
from src.core.config import settings

router = APIRouter()


class Cookies(BaseModel):
    uid: str
    did: str
    state: str
    verifier: str


CANVA_APP_ID = settings.CANVA_APP_ID
CANVA_CLIENT_ID = settings.CANVA_CLIENT_ID
CANVA_CLIENT_SECRET = settings.CANVA_CLIENT_SECRET
CANVA_AUTH_URL = "https://www.canva.com/api/oauth/authorize?code_challenge_method=s256&response_type=code&client_id={}&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Fapi%2Fv1%2Fauth%2Foauth%2Fredirect&scope=design:meta:read%20app:read%20design:permission:write%20asset:read%20design:content:read%20design:content:write%20asset:write%20design:permission:read%20app:write&code_challenge={}&state={}"

SESSION_COOKIE_NAME = "session"

templates = Jinja2Templates(directory="src/templates")

verifier_store = {}
state_store = {}
code_store = {}
tmp_user = {}


@router.get("/authorize/{user_id}")
async def get_auth_link(
    user_id: str,
    response: Response,
    uid: Annotated[str | None, Cookie()] = None,
    cookies: Annotated[Cookies | None, Cookie()] = None,
    test_cookie: Annotated[str | None, Cookie()] = None,
):
    verifier = await generate_code_verifier()
    state = await generate_code_verifier()
    print(f"UID: {uid}")
    print(f"Test Cookie: {test_cookie}")
    if cookies is not None:
        print(cookies)
        print(cookies.uid)
    state_store[state] = True
    verifier_store[state] = verifier
    tmp_user[state] = user_id
    code_challenge = await generate_code_challenge(verifier)
    url = CANVA_AUTH_URL.format(CANVA_CLIENT_ID, code_challenge, state)
    response.set_cookie(
        key="state",
        value=state,
        httponly=True,
        max_age=1000 * 60 * 60 * 20,
        samesite="lax",
    )
    response.set_cookie(
        key="verifier",
        value=verifier,
        httponly=True,
        max_age=1000 * 60 * 60 * 20,
        samesite="lax",
    )
    return {"url": url}


@router.get("/oauth/redirect")
async def redirect(
    request: Request,
    code: str = Query(..., description="code"),
    state: Optional[str] = Query(...),
    cookies: Annotated[Cookies | None, Cookie()] = None,
    db: Session = Depends(get_db),
):
    if state:
        if state not in state_store:
            raise HTTPException(
                status_code=403,
                detail="State parameter mismatch. Possible cross-site request forgery detected.",
            )

    code_store[state] = code
    token = await get_access_token_from_code(verifier_store[state], code)
    user_id = tmp_user[state]

    token_data = crud.set_auth_token(
        db,
        user_id=user_id,
        access_token=token["access_token"],
        refresh_token=token["refresh_token"],
        expires_in=datetime.now(timezone.utc) + timedelta(seconds=token["expires_in"]),
        scopes=token["scope"],
        jsonfile=token,
    )

    return RedirectResponse("/api/v1/auth/success")


@router.get("/success", response_class=HTMLResponse)
async def success(request: Request):
    return templates.TemplateResponse(
        "auth_success.html",
        {"request": request, "countdownSecs": 2, "message": "authorization_success"},
    )


@router.post("/{design_token}")
async def handle_request(
    request: Request,
    design_token: str,
    response: Response,
    authorization: str = Header(None),
):
    user_token = get_token_from_header(authorization)
    if not user_token or not design_token:
        raise HTTPException(status_code=401, detail="Missing tokens")

    try:
        user_payload = await verify_token(user_token)
    except Exception as e:
        raise HTTPException(
            status_code=401, detail=f"User Token verification failed: {str(e)}"
        )

    try:
        design_payload = await verify_token(design_token)
    except Exception as e:
        raise HTTPException(
            status_code=401, detail=f"Design Token verification failed: {str(e)}"
        )

    user_id = user_payload.get("userId")
    design_id = design_payload.get("designId")

    response.set_cookie("test_cookie", "test_value", httponly=True)
    response.set_cookie(
        key="uid", value=user_id, max_age=1000 * 60 * 60 * 24 * 3, httponly=True
    )
    response.set_cookie(
        key="did", value=design_id, max_age=1000 * 60 * 60 * 24 * 3, httponly=True
    )

    return {"user_id": user_id, "design_id": design_id}


@router.get("/is_authorized")
async def is_authorized(request: Request, user_id, db: Session = Depends(get_db)):
    print(request)
    uid = user_id
    access_token = getAccessToken(db, uid)
    if access_token is not None:
        return {"authorized": "true"}
    else:
        raise HTTPException(status_code=404)
