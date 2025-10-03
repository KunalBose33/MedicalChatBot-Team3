from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.integrations import google_auth
from app.core.security import create_access_token
from app.schemas.auth import Token
from app.models.user import User  # adjust import path to your User model

router = APIRouter(prefix="/auth/google", tags=["auth-google"])

@router.get("/login")
def google_login():
    return RedirectResponse(google_auth.get_google_login_url())

@router.get("/callback", response_model=Token)
def google_callback(code: str, db: Session = Depends(get_db)):
    profile = google_auth.exchange_code_for_userinfo(code)
    email = profile.get("email")
    sub = profile.get("sub")
    name = profile.get("name")
    picture = profile.get("picture")

    if not email:
        raise HTTPException(status_code=400, detail="No email from Google")

    # Upsert user
    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(email=email, name=name, picture=picture, provider="google", provider_id=sub)
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        user.name, user.picture = name, picture
        user.provider, user.provider_id = "google", sub
        db.commit()
        db.refresh(user)

    token = create_access_token({"sub": str(user.id), "email": user.email})
    return {"access_token": token, "token_type": "bearer"}
