"""
Authentication dependencies for FastAPI endpoints.

This module provides reusable dependencies for user authentication
that can be used across all protected endpoints.
"""

from typing import Optional
from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.models.models import User
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.framework.fastapi import verify_session


async def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
) -> User:
    """
    Get the current authenticated user from either SuperTokens session or dev API key.

    This dependency can be used in any endpoint that requires authentication:

    Example:
        @router.get("/my-endpoint")
        async def my_endpoint(current_user: User = Depends(get_current_user)):
            return {"user_id": current_user.id}

    Args:
        request: FastAPI request object
        db: Database session

    Returns:
        User: The authenticated user object

    Raises:
        HTTPException: 401 if not authenticated, 404 if user not found
    """
    # Check if this is a dev API key request (set by middleware)
    if hasattr(request.state, "dev_user_id"):
        user = db.query(User).filter(User.id == request.state.dev_user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Dev user not found"
            )
        return user

    # Otherwise, use SuperTokens session
    try:
        session: SessionContainer = await verify_session()(request)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    # Get SuperTokens user ID from session
    supertokens_user_id = session.get_user_id()

    # Also check for custom user_id in access token payload as fallback
    payload = session.get_access_token_payload()
    custom_user_id = payload.get("user_id")

    # Try to find user by supertokens_user_id first
    user = db.query(User).filter(User.supertokens_user_id == supertokens_user_id).first()

    # Fallback to custom user_id if not found
    if not user and custom_user_id:
        user = db.query(User).filter(User.id == custom_user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get the current authenticated user and verify they are active.

    Example:
        @router.get("/my-endpoint")
        async def my_endpoint(current_user: User = Depends(get_current_active_user)):
            return {"user_id": current_user.id}

    Args:
        current_user: The authenticated user from get_current_user

    Returns:
        User: The authenticated active user object

    Raises:
        HTTPException: 403 if user is inactive
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user


async def get_current_admin_user(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """
    Get the current authenticated user and verify they are an admin.

    Example:
        @router.get("/admin-only")
        async def admin_endpoint(admin_user: User = Depends(get_current_admin_user)):
            return {"admin_id": admin_user.id}

    Args:
        current_user: The authenticated active user from get_current_active_user

    Returns:
        User: The authenticated admin user object

    Raises:
        HTTPException: 403 if user is not an admin
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user


def get_optional_current_user(
    request: Request,
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Get the current user if authenticated, otherwise return None.
    Useful for endpoints that work differently for authenticated vs anonymous users.

    Example:
        @router.get("/public-endpoint")
        async def public_endpoint(user: Optional[User] = Depends(get_optional_current_user)):
            if user:
                return {"message": f"Hello {user.username}"}
            return {"message": "Hello anonymous user"}

    Args:
        request: FastAPI request object
        db: Database session

    Returns:
        Optional[User]: The authenticated user object or None
    """
    try:
        # This is a sync wrapper, but get_current_user is async
        # For optional user, we'll need to handle this differently
        # Check if dev API key is set
        if hasattr(request.state, "dev_user_id"):
            return db.query(User).filter(User.id == request.state.dev_user_id).first()

        # For SuperTokens, this would need to be async
        # For now, return None if no dev user
        return None
    except:
        return None
