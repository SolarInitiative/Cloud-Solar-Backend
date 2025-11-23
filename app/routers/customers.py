from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.core.auth_dependencies import get_current_user
from app.models.models import PanelOwnership, CustomerConsumption, EnergyCredits, Transaction, Notification, User
from app.schemas.schemas import (
    PanelOwnershipCreate, PanelOwnershipUpdate, PanelOwnershipResponse,
    CustomerConsumptionCreate, CustomerConsumptionUpdate, CustomerConsumptionResponse,
    EnergyCreditsCreate, EnergyCreditsUpdate, EnergyCreditsResponse,
    TransactionCreate, TransactionUpdate, TransactionResponse,
    NotificationCreate, NotificationUpdate, NotificationResponse,
    PaginationParams
)

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)

# --- Panel Ownership Endpoints ---

@router.post("/ownership/", response_model=PanelOwnershipResponse, status_code=status.HTTP_201_CREATED)
async def create_panel_ownership(
    ownership: PanelOwnershipCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_ownership = PanelOwnership(**ownership.dict())
    db.add(db_ownership)
    db.commit()
    db.refresh(db_ownership)
    return db_ownership

@router.get("/ownership/", response_model=List[PanelOwnershipResponse])
async def read_panel_ownerships(
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    ownerships = db.query(PanelOwnership).offset(pagination.skip).limit(pagination.limit).all()
    return ownerships

@router.get("/ownership/{ownership_id}", response_model=PanelOwnershipResponse)
async def read_panel_ownership(
    ownership_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    ownership = db.query(PanelOwnership).filter(PanelOwnership.ownership_id == ownership_id).first()
    if ownership is None:
        raise HTTPException(status_code=404, detail="Panel Ownership not found")
    return ownership

@router.put("/ownership/{ownership_id}", response_model=PanelOwnershipResponse)
async def update_panel_ownership(
    ownership_id: int,
    ownership_update: PanelOwnershipUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_ownership = db.query(PanelOwnership).filter(PanelOwnership.ownership_id == ownership_id).first()
    if db_ownership is None:
        raise HTTPException(status_code=404, detail="Panel Ownership not found")
    
    update_data = ownership_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_ownership, key, value)
    
    db.commit()
    db.refresh(db_ownership)
    return db_ownership

@router.delete("/ownership/{ownership_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_panel_ownership(
    ownership_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_ownership = db.query(PanelOwnership).filter(PanelOwnership.ownership_id == ownership_id).first()
    if db_ownership is None:
        raise HTTPException(status_code=404, detail="Panel Ownership not found")
    
    db.delete(db_ownership)
    db.commit()
    return None

# --- Customer Consumption Endpoints ---

@router.post("/consumption/", response_model=CustomerConsumptionResponse, status_code=status.HTTP_201_CREATED)
async def create_customer_consumption(
    consumption: CustomerConsumptionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_consumption = CustomerConsumption(**consumption.dict())
    db.add(db_consumption)
    db.commit()
    db.refresh(db_consumption)
    return db_consumption

@router.get("/consumption/", response_model=List[CustomerConsumptionResponse])
async def read_customer_consumptions(
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    consumptions = db.query(CustomerConsumption).offset(pagination.skip).limit(pagination.limit).all()
    return consumptions

@router.get("/consumption/{consumption_id}", response_model=CustomerConsumptionResponse)
async def read_customer_consumption(
    consumption_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    consumption = db.query(CustomerConsumption).filter(CustomerConsumption.consumption_id == consumption_id).first()
    if consumption is None:
        raise HTTPException(status_code=404, detail="Customer Consumption not found")
    return consumption

@router.put("/consumption/{consumption_id}", response_model=CustomerConsumptionResponse)
async def update_customer_consumption(
    consumption_id: int,
    consumption_update: CustomerConsumptionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_consumption = db.query(CustomerConsumption).filter(CustomerConsumption.consumption_id == consumption_id).first()
    if db_consumption is None:
        raise HTTPException(status_code=404, detail="Customer Consumption not found")
    
    update_data = consumption_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_consumption, key, value)
    
    db.commit()
    db.refresh(db_consumption)
    return db_consumption

@router.delete("/consumption/{consumption_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer_consumption(
    consumption_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_consumption = db.query(CustomerConsumption).filter(CustomerConsumption.consumption_id == consumption_id).first()
    if db_consumption is None:
        raise HTTPException(status_code=404, detail="Customer Consumption not found")
    
    db.delete(db_consumption)
    db.commit()
    return None

# --- Energy Credits Endpoints ---

@router.post("/credits/", response_model=EnergyCreditsResponse, status_code=status.HTTP_201_CREATED)
async def create_energy_credit(
    credit: EnergyCreditsCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_credit = EnergyCredits(**credit.dict())
    db.add(db_credit)
    db.commit()
    db.refresh(db_credit)
    return db_credit

@router.get("/credits/", response_model=List[EnergyCreditsResponse])
async def read_energy_credits(
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    credits = db.query(EnergyCredits).offset(pagination.skip).limit(pagination.limit).all()
    return credits

@router.get("/credits/{credit_id}", response_model=EnergyCreditsResponse)
async def read_energy_credit(
    credit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    credit = db.query(EnergyCredits).filter(EnergyCredits.credit_id == credit_id).first()
    if credit is None:
        raise HTTPException(status_code=404, detail="Energy Credit not found")
    return credit

@router.put("/credits/{credit_id}", response_model=EnergyCreditsResponse)
async def update_energy_credit(
    credit_id: int,
    credit_update: EnergyCreditsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_credit = db.query(EnergyCredits).filter(EnergyCredits.credit_id == credit_id).first()
    if db_credit is None:
        raise HTTPException(status_code=404, detail="Energy Credit not found")
    
    update_data = credit_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_credit, key, value)
    
    db.commit()
    db.refresh(db_credit)
    return db_credit

@router.delete("/credits/{credit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_energy_credit(
    credit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_credit = db.query(EnergyCredits).filter(EnergyCredits.credit_id == credit_id).first()
    if db_credit is None:
        raise HTTPException(status_code=404, detail="Energy Credit not found")
    
    db.delete(db_credit)
    db.commit()
    return None

# --- Transaction Endpoints ---

@router.post("/transactions/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_transaction = Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@router.get("/transactions/", response_model=List[TransactionResponse])
async def read_transactions(
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    transactions = db.query(Transaction).offset(pagination.skip).limit(pagination.limit).all()
    return transactions

@router.get("/transactions/{transaction_id}", response_model=TransactionResponse)
async def read_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    transaction = db.query(Transaction).filter(Transaction.transaction_id == transaction_id).first()
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@router.put("/transactions/{transaction_id}", response_model=TransactionResponse)
async def update_transaction(
    transaction_id: int,
    transaction_update: TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_transaction = db.query(Transaction).filter(Transaction.transaction_id == transaction_id).first()
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    update_data = transaction_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_transaction, key, value)
    
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@router.delete("/transactions/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_transaction = db.query(Transaction).filter(Transaction.transaction_id == transaction_id).first()
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    db.delete(db_transaction)
    db.commit()
    return None

# --- Notification Endpoints ---

@router.post("/notifications/", response_model=NotificationResponse, status_code=status.HTTP_201_CREATED)
async def create_notification(
    notification: NotificationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_notification = Notification(**notification.dict())
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification

@router.get("/notifications/", response_model=List[NotificationResponse])
async def read_notifications(
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    notifications = db.query(Notification).offset(pagination.skip).limit(pagination.limit).all()
    return notifications

@router.get("/notifications/{notification_id}", response_model=NotificationResponse)
async def read_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    notification = db.query(Notification).filter(Notification.notification_id == notification_id).first()
    if notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification

@router.put("/notifications/{notification_id}", response_model=NotificationResponse)
async def update_notification(
    notification_id: int,
    notification_update: NotificationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_notification = db.query(Notification).filter(Notification.notification_id == notification_id).first()
    if db_notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    update_data = notification_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_notification, key, value)
    
    db.commit()
    db.refresh(db_notification)
    return db_notification

@router.delete("/notifications/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_notification = db.query(Notification).filter(Notification.notification_id == notification_id).first()
    if db_notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    db.delete(db_notification)
    db.commit()
    return None
