from fastapi import FastAPI
from app.routers import health, auth, user 

app = FastAPI(title="Cloud Solar Backend")

# Include routers
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(user.router)