from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Numeric, Date, Float
from sqlalchemy.sql import func
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    phone = Column(String(20), nullable=True)
    address = Column(String, nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    postal_code = Column(String(20), nullable=True)
    is_admin = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    utility_provider = Column(String(100), nullable=True)
    utility_account_number = Column(String(100), nullable=True)
    registration_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    account_status = Column(String(20), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    location = Column(String, nullable=True)
    location_of_asset = Column(String, nullable=True)





    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}', is_admin={self.is_admin})>"


class SolarFarm(Base):
    __tablename__ = "solar_farms"

    farm_id = Column(Integer, primary_key=True, index=True)
    farm_name = Column(String(255), nullable=False)
    location_address = Column(Text, nullable=True)
    latitude = Column(Numeric(10, 8), nullable=True)
    longitude = Column(Numeric(11, 8), nullable=True)
    total_capacity_kw = Column(Numeric(10, 2), nullable=True)
    available_capacity_kw = Column(Numeric(10, 2), nullable=True)
    land_lease_start_date = Column(Date, nullable=True)
    land_lease_end_date = Column(Date, nullable=True)
    land_owner = Column(String(255), nullable=True)
    operational_status = Column(String(20), nullable=True)
    commissioning_date = Column(Date, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class SolarPanel(Base):
    __tablename__ = "solar_panels"

    panel_id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, ForeignKey("solar_farms.farm_id"), nullable=True)
    panel_serial_number = Column(String(100), unique=True, nullable=True)
    manufacturer = Column(String(100), nullable=True)
    model = Column(String(100), nullable=True)
    capacity_watts = Column(Numeric(8, 2), nullable=True)
    manufacture_date = Column(Date, nullable=True)
    installation_date = Column(Date, nullable=True)
    warranty_expiry_date = Column(Date, nullable=True)
    panel_status = Column(String(20), nullable=True)
    orientation = Column(String(50), nullable=True)
    tilt_angle = Column(Numeric(5, 2), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class PanelOwnership(Base):
    __tablename__ = "panel_ownership"

    ownership_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    panel_id = Column(Integer, ForeignKey("solar_panels.panel_id"), nullable=True)
    ownership_type = Column(String(20), nullable=True)
    purchase_date = Column(Date, nullable=True)
    purchase_price = Column(Numeric(10, 2), nullable=True)
    lease_start_date = Column(Date, nullable=True)
    lease_end_date = Column(Date, nullable=True)
    monthly_lease_amount = Column(Numeric(10, 2), nullable=True)
    ownership_status = Column(String(20), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class EnergyGeneration(Base):
    __tablename__ = "energy_generation"

    generation_id = Column(Integer, primary_key=True, index=True)
    panel_id = Column(Integer, ForeignKey("solar_panels.panel_id"), nullable=True)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    energy_generated_kwh = Column(Numeric(10, 4), nullable=True)
    voltage = Column(Numeric(6, 2), nullable=True)
    current = Column(Numeric(6, 2), nullable=True)
    temperature = Column(Numeric(5, 2), nullable=True)
    irradiance = Column(Numeric(6, 2), nullable=True)
    efficiency_percentage = Column(Numeric(5, 2), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class CustomerConsumption(Base):
    __tablename__ = "customer_consumption"

    consumption_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # Month (use DATE to represent the month; populate as first day of month)
    month = Column(Date, nullable=False)
    # Consumption in kWh for the month
    energy_consumed_kwh = Column(Numeric(10, 4), nullable=True)
    # Total cost for the consumption in the month
    total_cost = Column(Numeric(10, 2), nullable=True)


class EnergyCredits(Base):
    __tablename__ = "energy_credits"

    credit_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    billing_period_start = Column(Date, nullable=False)
    billing_period_end = Column(Date, nullable=False)
    total_generated_kwh = Column(Numeric(10, 4), nullable=True)
    total_consumed_kwh = Column(Numeric(10, 4), nullable=True)
    net_energy_kwh = Column(Numeric(10, 4), nullable=True)
    credit_amount = Column(Numeric(10, 2), nullable=True)
    debit_amount = Column(Numeric(10, 2), nullable=True)
    net_amount = Column(Numeric(10, 2), nullable=True)
    grid_rate_per_kwh = Column(Numeric(6, 4), nullable=True)
    status = Column(String(20), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class MaintenanceRecord(Base):
    __tablename__ = "maintenance_records"

    maintenance_id = Column(Integer, primary_key=True, index=True)
    panel_id = Column(Integer, ForeignKey("solar_panels.panel_id"), nullable=True)
    farm_id = Column(Integer, ForeignKey("solar_farms.farm_id"), nullable=True)
    maintenance_type = Column(String(50), nullable=True)
    scheduled_date = Column(Date, nullable=True)
    completed_date = Column(Date, nullable=True)
    description = Column(Text, nullable=True)
    technician_name = Column(String(100), nullable=True)
    cost = Column(Numeric(10, 2), nullable=True)
    status = Column(String(20), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    transaction_type = Column(String(30), nullable=True)
    amount = Column(Numeric(10, 2), nullable=True)
    transaction_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    payment_method = Column(String(50), nullable=True)
    payment_status = Column(String(20), nullable=True)
    reference_id = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Notification(Base):
    __tablename__ = "notifications"

    notification_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    notification_type = Column(String(50), nullable=True)
    title = Column(String(255), nullable=True)
    message = Column(Text, nullable=True)
    priority = Column(String(20), nullable=True)
    is_read = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
