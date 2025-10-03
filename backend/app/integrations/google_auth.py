import httpx
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.settings import settings
from app.db.session import get_db
from app.db import base  # contains User model if imported
from app.schemas.auth import Token
from app.core.security import create_access_token  # you already have for Entra/local auth

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"

def get_google_login_url():
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "response_type": "code",
        "scope": "openid email profile",
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "access_type": "offline",
        "include_granted_scopes": "true",
    }
    import urllib.parse
    return f"{GOOGLE_AUTH_URL}?{urllib.parse.urlencode(params)}"

def exchange_code_for_userinfo(code: str):
    data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    with httpx.Client() as client:
        token_resp = client.post(GOOGLE_TOKEN_URL, data=data)
        if token_resp.status_code != 200:
            raise HTTPException(status_code=400, detail="Google token exchange failed")
        token_json = token_resp.json()
        access_token = token_json.get("access_token")

        userinfo_resp = client.get(GOOGLE_USERINFO_URL, headers={"Authorization": f"Bearer {access_token}"})
        if userinfo_resp.status_code != 200:
            raise HTTPException(status_code=400, detail="Google userinfo fetch failed")
        return userinfo_resp.json()
