from fastapi import FastAPI
from app.routers import health, auth

app = FastAPI(title="Cloud Solar Backend")

# Include routers
app.include_router(health.router)
app.include_router(auth.router)

# Optional root route
@app.get("/")
def read_root():
    return {"message": "Welcome to Cloud Solar Backend"}
