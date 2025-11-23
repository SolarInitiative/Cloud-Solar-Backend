"""
Custom middleware for authentication and request processing.
"""

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp


class DevAPIKeyMiddleware(BaseHTTPMiddleware):
    """
    Middleware to handle development API key authentication.

    When a request includes the header "X-API-Key: dev_api_key_123",
    it bypasses JWT authentication and assigns a default dev user.

    This is useful for:
    - Development and testing
    - API testing tools (Postman, curl, etc.)
    - Automated tests

    IMPORTANT: This should only be enabled in development environments!
    """

    def __init__(self, app: ASGIApp, dev_user_id: int = 1):
        """
        Initialize the middleware.

        Args:
            app: The ASGI application
            dev_user_id: The default user ID to use for dev API key requests
        """
        super().__init__(app)
        self.dev_user_id = dev_user_id
        self.dev_api_key = "dev_api_key_123"

    async def dispatch(self, request: Request, call_next) -> Response:
        """
        Process the request and check for dev API key.

        Args:
            request: The incoming request
            call_next: The next middleware/endpoint in the chain

        Returns:
            Response: The response from the endpoint
        """
        # Check for dev API key in headers
        api_key = request.headers.get("X-API-Key")

        if api_key == self.dev_api_key:
            # Set a flag on request state to indicate this is a dev API key request
            request.state.dev_user_id = self.dev_user_id
            request.state.is_dev_mode = True

        # Continue processing the request
        response = await call_next(request)
        return response
