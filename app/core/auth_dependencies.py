"""
Authentication dependencies for protected routes.
This module has been updated to remove SuperTokens and use JWT-based authentication.
"""

from fastapi import Depends, HTTPException, status, Request, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional
from app.db.base import get_db
from app.models.models import User
from app.core.security import verify_token

security = HTTPBearer(auto_error=False)


async def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to get the current authenticated user.
    Supports both JWT Bearer token and Dev API Key.

    Args:
        request: The FastAPI request object
        credentials: HTTP Bearer token from Authorization header (optional)
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
    
    # 2. Check for JWT Bearer Token
    elif credentials:
        payload = verify_token(credentials.credentials)
        if payload:
            user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Fetch user from database
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
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


async def get_current_user_optional(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Dependency for optional authentication.
    Returns user if authenticated, None otherwise.

    Args:
        request: The FastAPI request object
        credentials: HTTP Bearer token from Authorization header (optional)
        db: Database session

    Returns:
        User or None
    """
    user_id = None

    # 1. Check for Dev API Key (via middleware state)
    if hasattr(request.state, "is_dev_mode") and request.state.is_dev_mode:
        user_id = request.state.dev_user_id
    
    # 2. Check for JWT Bearer Token
    elif credentials:
        payload = verify_token(credentials.credentials)
        if payload:
            user_id = payload.get("sub")

    if not user_id:
        return None

    # Fetch user from database
    user = db.query(User).filter(User.id == user_id).first()
    
    if user and user.is_active:
        return user
    
    return None
