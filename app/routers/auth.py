from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.models.models import User
from app.schemas.auth import SignupRequest, LoginRequest, TokenResponse, UserResponse
from app.core.security import verify_password, create_access_token, get_password_hash
from datetime import timedelta
from supertokens_python.recipe.emailpassword.asyncio import sign_up, sign_in
from supertokens_python.recipe.emailpassword.interfaces import SignUpOkResult, SignInOkResult
from supertokens_python.recipe.session.asyncio import create_new_session
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.framework.fastapi import verify_session

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    request: Request,
    signup_data: SignupRequest,
    db: Session = Depends(get_db)
):
    """
    User registration endpoint with SuperTokens integration.

    Args:
        request: FastAPI request object
        response: FastAPI response object
        signup_data: User registration data (username, email, password, etc.)
        db: Database session

    Returns:
        Created user information

    Raises:
        HTTPException: If username or email already exists
    """
    # Check if username already exists
    existing_user = db.query(User).filter(User.username == signup_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    # Check if email already exists
    existing_email = db.query(User).filter(User.email == signup_data.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Sign up with SuperTokens
    supertokens_result = await sign_up("public", signup_data.email, signup_data.password)

    if not isinstance(supertokens_result, SignUpOkResult):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered with SuperTokens"
        )

    # Create new user in your database
    hashed_password = get_password_hash(signup_data.password)
    new_user = User(
        username=signup_data.username,
        email=signup_data.email,
        hashed_password=hashed_password,
        full_name=signup_data.full_name,
        location=signup_data.location,
        is_active=True,
        is_admin=False
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Create session for the user
    await create_new_session(
        request=request,
        tenant_id="public",
        user_id=supertokens_result.user.id,
        access_token_payload={
            "user_id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
            "is_admin": new_user.is_admin
        },
        session_data_in_database={}
    )

    return new_user


@router.post("/login")
async def login(
    request: Request,
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login endpoint for user authentication with SuperTokens integration.

    Args:
        request: FastAPI request object
        response: FastAPI response object
        login_data: Login credentials (username and password)
        db: Database session

    Returns:
        Success message with session cookies set

    Raises:
        HTTPException: If credentials are invalid or user is inactive
    """
    # Find user by username
    user = db.query(User).filter(User.username == login_data.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user account",
        )

    # Sign in with SuperTokens using email
    supertokens_result = await sign_in("public", user.email, login_data.password)

    if not isinstance(supertokens_result, SignInOkResult):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create session for the user
    await create_new_session(
        request=request,
        tenant_id="public",
        user_id=supertokens_result.user.id,
        access_token_payload={
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "is_admin": user.is_admin
        },
        session_data_in_database={}
    )

    return {
        "status": "OK",
        "message": "Login successful",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_admin": user.is_admin
        }
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    session: SessionContainer = Depends(verify_session()),
    db: Session = Depends(get_db)
):
    """
    Get current authenticated user information using SuperTokens session.

    Args:
        session: SuperTokens session container with user session data
        db: Database session

    Returns:
        Current user information

    Raises:
        HTTPException: If user not found
    """
    # Get user ID from session payload
    user_id = session.get_access_token_payload().get("user_id")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found in session"
        )

    # Fetch user from database
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


@router.post("/logout")
async def logout(session: SessionContainer = Depends(verify_session())):
    """
    Logout endpoint to revoke the current session.

    Args:
        session: SuperTokens session container

    Returns:
        Success message
    """
    await session.revoke_session()
    return {"status": "OK", "message": "Logout successful"}
