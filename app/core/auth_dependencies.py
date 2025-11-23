"""
Authentication dependencies for protected routes using SuperTokens.
"""

from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.framework.fastapi import verify_session
from app.db.base import get_db
from app.models.models import User


async def get_current_user(
    request: Request,
    session: SessionContainer = Depends(verify_session(session_required=False)),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to get the current authenticated user.
    Supports both SuperTokens session and Dev API Key.

    Args:
        request: The FastAPI request object
        session: SuperTokens session container (optional)
        db: Database session

    Returns:
        User: Current authenticated user

    Raises:
        HTTPException: If user not found or not authenticated
    """
    user_id = None

    # 1. Check for Dev API Key (via middleware state)
    if hasattr(request.state, "is_dev_mode") and request.state.is_dev_mode:
        user_id = request.state.dev_user_id
    
    # 2. Check for SuperTokens Session
    elif session:
        user_id = session.get_access_token_payload().get("user_id")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )

    # Fetch user from database
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        # If it's a supertokens user but not in our DB yet, we might handle that differently
        # But for now, we expect the user to exist
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    return user


async def get_current_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency to verify the current user is an admin.

    Args:
        current_user: Current authenticated user

    Returns:
        User: Current admin user

    Raises:
        HTTPException: If user is not an admin
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )

    return current_user


def get_optional_session():
    """
    Dependency for optional authentication.
    Returns session if valid, None otherwise.
    """
    return verify_session(session_required=False)
