from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.core.auth_dependencies import get_current_user
from app.models.models import SolarFarm, SolarPanel, MaintenanceRecord, User
from app.schemas.schemas import (
    SolarFarmCreate, SolarFarmUpdate, SolarFarmResponse,
    SolarPanelCreate, SolarPanelUpdate, SolarPanelResponse,
    MaintenanceRecordCreate, MaintenanceRecordUpdate, MaintenanceRecordResponse,
    PaginationParams
)

router = APIRouter(
    prefix="/farms",
    tags=["Solar Farms"]
)

# --- Solar Farm Endpoints ---

@router.post("/", response_model=SolarFarmResponse, status_code=status.HTTP_201_CREATED)
async def create_solar_farm(
    farm: SolarFarmCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_farm = SolarFarm(**farm.dict())
    db.add(db_farm)
    db.commit()
    db.refresh(db_farm)
    return db_farm

@router.get("/", response_model=List[SolarFarmResponse])
async def read_solar_farms(
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    farms = db.query(SolarFarm).offset(pagination.skip).limit(pagination.limit).all()
    return farms

@router.get("/{farm_id}", response_model=SolarFarmResponse)
async def read_solar_farm(
    farm_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    farm = db.query(SolarFarm).filter(SolarFarm.farm_id == farm_id).first()
    if farm is None:
        raise HTTPException(status_code=404, detail="Solar Farm not found")
    return farm

@router.put("/{farm_id}", response_model=SolarFarmResponse)
async def update_solar_farm(
    farm_id: int,
    farm_update: SolarFarmUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_farm = db.query(SolarFarm).filter(SolarFarm.farm_id == farm_id).first()
    if db_farm is None:
        raise HTTPException(status_code=404, detail="Solar Farm not found")
    
    update_data = farm_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_farm, key, value)
    
    db.commit()
    db.refresh(db_farm)
    return db_farm

@router.delete("/{farm_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_solar_farm(
    farm_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_farm = db.query(SolarFarm).filter(SolarFarm.farm_id == farm_id).first()
    if db_farm is None:
        raise HTTPException(status_code=404, detail="Solar Farm not found")
    
    db.delete(db_farm)
    db.commit()
    return None

# --- Solar Panel Endpoints ---

@router.post("/panels/", response_model=SolarPanelResponse, status_code=status.HTTP_201_CREATED)
async def create_solar_panel(
    panel: SolarPanelCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_panel = SolarPanel(**panel.dict())
    db.add(db_panel)
    db.commit()
    db.refresh(db_panel)
    return db_panel

@router.get("/panels/", response_model=List[SolarPanelResponse])
async def read_solar_panels(
    farm_id: Optional[int] = None,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(SolarPanel)
    if farm_id:
        query = query.filter(SolarPanel.farm_id == farm_id)
    panels = query.offset(pagination.skip).limit(pagination.limit).all()
    return panels

@router.get("/panels/{panel_id}", response_model=SolarPanelResponse)
async def read_solar_panel(
    panel_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    panel = db.query(SolarPanel).filter(SolarPanel.panel_id == panel_id).first()
    if panel is None:
        raise HTTPException(status_code=404, detail="Solar Panel not found")
    return panel

@router.put("/panels/{panel_id}", response_model=SolarPanelResponse)
async def update_solar_panel(
    panel_id: int,
    panel_update: SolarPanelUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_panel = db.query(SolarPanel).filter(SolarPanel.panel_id == panel_id).first()
    if db_panel is None:
        raise HTTPException(status_code=404, detail="Solar Panel not found")
    
    update_data = panel_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_panel, key, value)
    
    db.commit()
    db.refresh(db_panel)
    return db_panel

@router.delete("/panels/{panel_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_solar_panel(
    panel_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_panel = db.query(SolarPanel).filter(SolarPanel.panel_id == panel_id).first()
    if db_panel is None:
        raise HTTPException(status_code=404, detail="Solar Panel not found")
    
    db.delete(db_panel)
    db.commit()
    return None

# --- Maintenance Record Endpoints ---

@router.post("/maintenance/", response_model=MaintenanceRecordResponse, status_code=status.HTTP_201_CREATED)
async def create_maintenance_record(
    record: MaintenanceRecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_record = MaintenanceRecord(**record.dict())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

@router.get("/maintenance/", response_model=List[MaintenanceRecordResponse])
async def read_maintenance_records(
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    records = db.query(MaintenanceRecord).offset(pagination.skip).limit(pagination.limit).all()
    return records

@router.get("/maintenance/{maintenance_id}", response_model=MaintenanceRecordResponse)
async def read_maintenance_record(
    maintenance_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    record = db.query(MaintenanceRecord).filter(MaintenanceRecord.maintenance_id == maintenance_id).first()
    if record is None:
        raise HTTPException(status_code=404, detail="Maintenance Record not found")
    return record

@router.put("/maintenance/{maintenance_id}", response_model=MaintenanceRecordResponse)
async def update_maintenance_record(
    maintenance_id: int,
    record_update: MaintenanceRecordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_record = db.query(MaintenanceRecord).filter(MaintenanceRecord.maintenance_id == maintenance_id).first()
    if db_record is None:
        raise HTTPException(status_code=404, detail="Maintenance Record not found")
    
    update_data = record_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_record, key, value)
    
    db.commit()
    db.refresh(db_record)
    return db_record

@router.delete("/maintenance/{maintenance_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_maintenance_record(
    maintenance_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_record = db.query(MaintenanceRecord).filter(MaintenanceRecord.maintenance_id == maintenance_id).first()
    if db_record is None:
        raise HTTPException(status_code=404, detail="Maintenance Record not found")
    
    db.delete(db_record)
    db.commit()
    return None
