from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.auth_dependencies import get_current_user, get_current_admin_user
from app.models.models import User
from app.db.base import get_db
from app.schemas.auth import UserResponse

router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@router.get("/me", response_model=UserResponse, summary="Get current logged-in user")
async def get_logged_in_user(
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve details of the currently logged-in user using SuperTokens session.

    This endpoint uses SuperTokens session verification to identify the user.
    The session is automatically validated via cookies or Authorization header.

    Returns:
        UserResponse: Current user information including id, username, email, etc.
    """
    return current_user


@router.get("/profile", response_model=UserResponse, summary="Get user profile")
async def get_user_profile(
    current_user: User = Depends(get_current_user)
):
    """
    Get the full profile of the currently logged-in user.

    Returns:
        UserResponse: Complete user profile information
    """
    return current_user


@router.get("/admin/test", summary="Test admin access")
async def test_admin_access(
    admin_user: User = Depends(get_current_admin_user)
):
    """
    Test endpoint to verify admin access.

    This endpoint requires admin privileges.

    Returns:
        Success message with admin user info
    """
    return {
        "status": "OK",
        "message": "Admin access granted",
        "admin": {
            "id": admin_user.id,
            "username": admin_user.username,
            "email": admin_user.email
        }
    }
