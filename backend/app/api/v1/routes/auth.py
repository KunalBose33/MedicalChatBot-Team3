from fastapi import APIRouter

router = APIRouter()

@router.get("/login")
def login():
    return {"message": "Microsoft Entra ID login endpoint placeholder"}

@router.get("/me")
def get_current_user():
    return {"user": "current user info placeholder"}
