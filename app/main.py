from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import health, auth, user, farms, customers, energy
from app.core.supertokens_config import init_supertokens, get_all_cors_headers
from app.core.middleware import DevAPIKeyMiddleware
from supertokens_python.framework.fastapi import get_middleware

# Initialize SuperTokens
init_supertokens()

app = FastAPI(title="Cloud Solar Backend")

# Add CORS middleware (first in chain, last to execute)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Update with your frontend URL
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "X-API-Key"] + get_all_cors_headers(),
)

# Add SuperTokens middleware (executes before dev API key middleware)
app.add_middleware(get_middleware())

# Add dev API key middleware (executes first, checks for dev key before SuperTokens)
# NOTE: In production, you should disable this or use environment variables to control it
app.add_middleware(DevAPIKeyMiddleware, dev_user_id=1)

# Include routers
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(farms.router)
app.include_router(customers.router)
app.include_router(energy.router)