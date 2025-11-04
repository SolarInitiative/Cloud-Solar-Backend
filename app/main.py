from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import health, auth, user
from app.core.supertokens_config import init_supertokens, get_all_cors_headers
from supertokens_python.framework.fastapi import get_middleware

# Initialize SuperTokens
init_supertokens()

app = FastAPI(title="Cloud Solar Backend")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Update with your frontend URL
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type"] + get_all_cors_headers(),
)

# Add SuperTokens middleware
app.add_middleware(get_middleware())

# Include routers
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(user.router)