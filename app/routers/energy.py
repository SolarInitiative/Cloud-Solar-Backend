from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.core.auth_dependencies import get_current_user
from app.models.models import EnergyGeneration, User
from app.schemas.schemas import (
    EnergyGenerationCreate, EnergyGenerationUpdate, EnergyGenerationResponse,
    PaginationParams
)

router = APIRouter(
    prefix="/energy",
    tags=["Energy Generation"]
)

# --- Energy Generation Endpoints ---

@router.post("/generation/", response_model=EnergyGenerationResponse, status_code=status.HTTP_201_CREATED)
async def create_energy_generation(
    generation: EnergyGenerationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_generation = EnergyGeneration(**generation.dict())
    db.add(db_generation)
    db.commit()
    db.refresh(db_generation)
    return db_generation

@router.get("/generation/", response_model=List[EnergyGenerationResponse])
async def read_energy_generations(
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    generations = db.query(EnergyGeneration).offset(pagination.skip).limit(pagination.limit).all()
    return generations

@router.get("/generation/{generation_id}", response_model=EnergyGenerationResponse)
async def read_energy_generation(
    generation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    generation = db.query(EnergyGeneration).filter(EnergyGeneration.generation_id == generation_id).first()
    if generation is None:
        raise HTTPException(status_code=404, detail="Energy Generation not found")
    return generation

@router.put("/generation/{generation_id}", response_model=EnergyGenerationResponse)
async def update_energy_generation(
    generation_id: int,
    generation_update: EnergyGenerationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_generation = db.query(EnergyGeneration).filter(EnergyGeneration.generation_id == generation_id).first()
    if db_generation is None:
        raise HTTPException(status_code=404, detail="Energy Generation not found")
    
    update_data = generation_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_generation, key, value)
    
    db.commit()
    db.refresh(db_generation)
    return db_generation

@router.delete("/generation/{generation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_energy_generation(
    generation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_generation = db.query(EnergyGeneration).filter(EnergyGeneration.generation_id == generation_id).first()
    if db_generation is None:
        raise HTTPException(status_code=404, detail="Energy Generation not found")
    
    db.delete(db_generation)
    db.commit()
    return None
