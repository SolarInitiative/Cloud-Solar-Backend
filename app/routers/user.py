from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.security import decode_access_token
from app.models import models
from app.db.base import get_db
import re

router = APIRouter(
    prefix="/user",
    tags=["User"]
)

# Reuse the same OAuth2 scheme used in your auth routes
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.get("/me", summary="Get current logged-in user")
def get_logged_in_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Retrieve details of the currently logged-in user using the JWT token.

    The token payload's 'sub' field can contain either an email or username.
    The function automatically determines which one it is and queries accordingly.
    """
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    identifier = payload.get("sub")
    if not identifier:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token data",
        )

    # Check if the identifier is an email or username
    email_pattern = r"[^@]+@[^@]+\.[^@]+"
    if re.match(email_pattern, identifier):
        user = db.query(models.User).filter(models.User.email == identifier).first()
    else:
        user = db.query(models.User).filter(models.User.username == identifier).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "created_at": user.created_at, 
        "location": user.location 
    }
