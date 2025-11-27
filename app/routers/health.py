from fastapi import APIRouter

router = APIRouter()

@router.get("/healthhh", tags=["Health Check"])
def health_check():
    return {"status": "healthy", "message": "Server is running fine!"}
