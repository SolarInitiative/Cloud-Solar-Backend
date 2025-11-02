from fastapi import FastAPI
from routers import health

app = FastAPI(title="Cloud Solar Backend")

# Include the health check router
app.include_router(health.router)

# Optional root route
@app.get("/")
def read_root():
    return {"message": "Welcome to Cloud Solar Backend"}
