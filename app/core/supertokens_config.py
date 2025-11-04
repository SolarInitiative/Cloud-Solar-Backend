"""
SuperTokens configuration for Cloud Solar application.
This module initializes SuperTokens with EmailPassword recipe for user authentication.
"""
from supertokens_python import get_all_cors_headers as supertokens_cors_headers


import os
from typing import Dict, Any
from supertokens_python import init, InputAppInfo, SupertokensConfig, get_all_cors_headers
from supertokens_python.recipe import emailpassword, session
from supertokens_python.recipe.emailpassword.interfaces import (
    APIInterface as EmailPasswordAPIInterface,
    APIOptions as EmailPasswordAPIOptions,
)
from supertokens_python.recipe.session.interfaces import (
    APIInterface as SessionAPIInterface,
    APIOptions as SessionAPIOptions,
)
from typing import Optional, Union
from supertokens_python.types import GeneralErrorResponse
from supertokens_python.recipe.emailpassword import EmailPasswordRecipe
from supertokens_python.recipe.session import SessionRecipe
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def override_email_password_apis(original_implementation: EmailPasswordAPIInterface):
    """
    Override EmailPassword APIs to disable built-in endpoints.
    We're using custom endpoints instead.
    """
    original_implementation.disable_sign_up_post = True
    original_implementation.disable_sign_in_post = True
    original_implementation.disable_email_exists_get = True
    original_implementation.disable_generate_password_reset_token_post = True
    original_implementation.disable_password_reset_post = True
    return original_implementation


def init_supertokens():
    """
    Initialize SuperTokens with EmailPassword and Session recipes.
    """

    supertokens_uri = os.getenv("SUPERTOKENS_CONNECTION_URI", "http://localhost:3567")
    api_domain = os.getenv("API_DOMAIN", "http://localhost:8000")
    website_domain = os.getenv("WEBSITE_DOMAIN", "http://localhost:3000")
    api_base_path = os.getenv("API_BASE_PATH", "/auth/st")
    website_base_path = os.getenv("WEBSITE_BASE_PATH", "/auth")

    init(
        supertokens_config=SupertokensConfig(
            connection_uri=supertokens_uri,
            api_key=os.getenv("SUPERTOKENS_API_KEY"),
        ),
        app_info=InputAppInfo(
            app_name="Cloud Solar",
            api_domain=api_domain,
            website_domain=website_domain,
            api_base_path=api_base_path,
            website_base_path=website_base_path,
        ),
        framework="fastapi",
        recipe_list=[
            emailpassword.init(
                override=emailpassword.InputOverrideConfig(
                    apis=override_email_password_apis
                )
            ),
            session.init(
                cookie_domain=os.getenv("COOKIE_DOMAIN"),
                cookie_same_site=os.getenv("COOKIE_SAME_SITE", "lax"),
                cookie_secure=os.getenv("COOKIE_SECURE", "false").lower() == "true",
                session_expired_status_code=401,
            ),
        ],
        mode="asgi",
    )


def get_all_cors_headers() -> list[str]:
    """
    Get all CORS headers required by SuperTokens.
    """
    return supertokens_cors_headers()
