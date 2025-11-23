from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import health, auth, user, farms, customers, energy
from app.core.middleware import DevAPIKeyMiddleware

app = FastAPI(title="Cloud Solar Backend")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Update with your frontend URL
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],  # Allow all headers including Authorization
)

# Add Dev API Key middleware for development
# This allows bypassing authentication with X-API-Key: dev_api_key_123 header
app.add_middleware(DevAPIKeyMiddleware, dev_user_id=1)

# Include routers
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(farms.router)
app.include_router(customers.router)
app.include_router(energy.router)