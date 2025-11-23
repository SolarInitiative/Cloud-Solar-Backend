from typing import Optional, List
from datetime import date, datetime
from pydantic import BaseModel, Field, EmailStr
from decimal import Decimal

# --- Shared Schemas ---

class PaginationParams(BaseModel):
    skip: int = 0
    limit: int = 100

# --- Solar Farm Schemas ---

class SolarFarmBase(BaseModel):
    farm_name: str
    location_address: Optional[str] = None
    total_capacity_kw: Optional[Decimal] = None
    available_panels: Optional[Decimal] = None
    land_lease_start_date: Optional[date] = None
    land_lease_end_date: Optional[date] = None
    land_owner: Optional[str] = None
    operational_status: Optional[str] = None

class SolarFarmCreate(SolarFarmBase):
    pass

class SolarFarmUpdate(SolarFarmBase):
    farm_name: Optional[str] = None

class SolarFarmResponse(SolarFarmBase):
    farm_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# --- Solar Panel Schemas ---

class SolarPanelBase(BaseModel):
    farm_id: Optional[int] = None
    panel_serial_number: Optional[str] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    capacity_watts: Optional[Decimal] = None
    manufacture_date: Optional[date] = None
    installation_date: Optional[date] = None
    warranty_expiry_date: Optional[date] = None
    panel_status: Optional[str] = None

class SolarPanelCreate(SolarPanelBase):
    pass

class SolarPanelUpdate(SolarPanelBase):
    pass

class SolarPanelResponse(SolarPanelBase):
    panel_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# --- Panel Ownership Schemas ---

class PanelOwnershipBase(BaseModel):
    customer_id: Optional[int] = None
    panel_id: Optional[int] = None
    ownership_type: Optional[str] = None
    ownership_status: Optional[str] = None
    purchase_date: Optional[date] = None
    purchase_price: Optional[Decimal] = None
    lease_start_date: Optional[date] = None
    lease_end_date: Optional[date] = None
    monthly_lease_amount: Optional[Decimal] = None

class PanelOwnershipCreate(PanelOwnershipBase):
    pass

class PanelOwnershipUpdate(PanelOwnershipBase):
    pass

class PanelOwnershipResponse(PanelOwnershipBase):
    ownership_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# --- Energy Generation Schemas ---

class EnergyGenerationBase(BaseModel):
    panel_id: Optional[int] = None
    timestamp: datetime
    energy_generated_kwh: Optional[Decimal] = None
    voltage: Optional[Decimal] = None
    current: Optional[Decimal] = None
    efficiency_percentage: Optional[Decimal] = None

class EnergyGenerationCreate(EnergyGenerationBase):
    pass

class EnergyGenerationUpdate(EnergyGenerationBase):
    pass

class EnergyGenerationResponse(EnergyGenerationBase):
    generation_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# --- Customer Consumption Schemas ---

class CustomerConsumptionBase(BaseModel):
    customer_id: int
    month: date
    energy_consumed_kwh: Optional[Decimal] = None
    total_cost: Optional[Decimal] = None

class CustomerConsumptionCreate(CustomerConsumptionBase):
    pass

class CustomerConsumptionUpdate(CustomerConsumptionBase):
    pass

class CustomerConsumptionResponse(CustomerConsumptionBase):
    consumption_id: int

    class Config:
        from_attributes = True

# --- Energy Credits Schemas ---

class EnergyCreditsBase(BaseModel):
    customer_id: Optional[int] = None
    billing_period_start: date
    billing_period_end: date
    total_generated_kwh: Optional[Decimal] = None
    total_consumed_kwh: Optional[Decimal] = None
    credit_amount: Optional[Decimal] = None
    debit_amount: Optional[Decimal] = None
    net_amount: Optional[Decimal] = None

class EnergyCreditsCreate(EnergyCreditsBase):
    pass

class EnergyCreditsUpdate(EnergyCreditsBase):
    pass

class EnergyCreditsResponse(EnergyCreditsBase):
    credit_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# --- Maintenance Record Schemas ---

class MaintenanceRecordBase(BaseModel):
    panel_id: Optional[int] = None
    farm_id: Optional[int] = None
    maintenance_type: Optional[str] = None
    scheduled_date: Optional[date] = None
    completed_date: Optional[date] = None
    description: Optional[str] = None

class MaintenanceRecordCreate(MaintenanceRecordBase):
    pass

class MaintenanceRecordUpdate(MaintenanceRecordBase):
    pass

class MaintenanceRecordResponse(MaintenanceRecordBase):
    maintenance_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# --- Transaction Schemas ---

class TransactionBase(BaseModel):
    customer_id: Optional[int] = None
    transaction_type: Optional[str] = None
    amount: Optional[Decimal] = None
    transaction_date: Optional[datetime] = None
    payment_method: Optional[str] = None
    payment_status: Optional[str] = None
    reference_id: Optional[str] = None
    description: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(TransactionBase):
    pass

class TransactionResponse(TransactionBase):
    transaction_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# --- Notification Schemas ---

class NotificationBase(BaseModel):
    customer_id: Optional[int] = None
    notification_type: Optional[str] = None
    title: Optional[str] = None
    message: Optional[str] = None
    priority: Optional[str] = None
    is_read: bool = False

class NotificationCreate(NotificationBase):
    pass

class NotificationUpdate(NotificationBase):
    pass

class NotificationResponse(NotificationBase):
    notification_id: int
    created_at: datetime

    class Config:
        from_attributes = True
