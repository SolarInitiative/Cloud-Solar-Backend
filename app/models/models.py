from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Numeric, Date, Float, Index, CheckConstraint
from sqlalchemy.orm import relationship
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
    location = Column(String, nullable=True)
    registration_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    account_status = Column(String(20), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    panel_ownerships = relationship("PanelOwnership", back_populates="customer")
    consumptions = relationship("CustomerConsumption", back_populates="customer")
    energy_credits = relationship("EnergyCredits", back_populates="customer")
    transactions = relationship("Transaction", back_populates="customer")
    notifications = relationship("Notification", back_populates="customer")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}', is_admin={self.is_admin})>"


class SolarFarm(Base):
    __tablename__ = "solar_farms"

    farm_id = Column(Integer, primary_key=True, index=True)
    farm_name = Column(String(255), nullable=False)
    location_address = Column(Text, nullable=True)
    total_capacity_kw = Column(Numeric(10, 2), nullable=True)
    available_panels = Column(Numeric(10, 2), nullable=True)
    land_lease_start_date = Column(Date, nullable=True)
    land_lease_end_date = Column(Date, nullable=True)
    land_owner = Column(String(255), nullable=True)
    operational_status = Column(String(20), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    panels = relationship("SolarPanel", back_populates="farm")
    maintenance_records = relationship("MaintenanceRecord", back_populates="farm")

    # Check constraint for date range
    __table_args__ = (
        CheckConstraint('land_lease_start_date IS NULL OR land_lease_end_date IS NULL OR land_lease_start_date <= land_lease_end_date',
                       name='check_lease_dates'),
    )


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
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    farm = relationship("SolarFarm", back_populates="panels")
    ownerships = relationship("PanelOwnership", back_populates="panel")
    energy_generations = relationship("EnergyGeneration", back_populates="panel")
    maintenance_records = relationship("MaintenanceRecord", back_populates="panel")


class PanelOwnership(Base):
    __tablename__ = "panel_ownership"

    ownership_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    panel_id = Column(Integer, ForeignKey("solar_panels.panel_id"), nullable=True)
    ownership_type = Column(String(20), nullable=True)
    ownership_status = Column(String(20), nullable=True)
    purchase_date = Column(Date, nullable=True)
    purchase_price = Column(Numeric(10, 2), nullable=True)
    lease_start_date = Column(Date, nullable=True)
    lease_end_date = Column(Date, nullable=True)
    monthly_lease_amount = Column(Numeric(10, 2), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    customer = relationship("User", back_populates="panel_ownerships")
    panel = relationship("SolarPanel", back_populates="ownerships")

    # Check constraint for lease dates
    __table_args__ = (
        CheckConstraint('lease_start_date IS NULL OR lease_end_date IS NULL OR lease_start_date <= lease_end_date',
                       name='check_ownership_lease_dates'),
    )


class EnergyGeneration(Base):
    __tablename__ = "energy_generation"

    generation_id = Column(Integer, primary_key=True, index=True)
    panel_id = Column(Integer, ForeignKey("solar_panels.panel_id"), nullable=True)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    energy_generated_kwh = Column(Numeric(10, 4), nullable=True)
    voltage = Column(Numeric(6, 2), nullable=True)
    current = Column(Numeric(6, 2), nullable=True)
    efficiency_percentage = Column(Numeric(5, 2), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    panel = relationship("SolarPanel", back_populates="energy_generations")

    # Composite index for efficient queries by panel and time
    __table_args__ = (
        Index('ix_energy_generation_panel_timestamp', 'panel_id', 'timestamp'),
    )


class CustomerConsumption(Base):
    __tablename__ = "customer_consumption"
    # Monthly energy consumption records for customers for Comparison with energy generated

    consumption_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    month = Column(Date, nullable=False)
    energy_consumed_kwh = Column(Numeric(10, 4), nullable=True)
    total_cost = Column(Numeric(10, 2), nullable=True)

    # Relationships
    customer = relationship("User", back_populates="consumptions")

    # Composite index for efficient queries by customer and month
    __table_args__ = (
        Index('ix_customer_consumption_customer_month', 'customer_id', 'month'),
    )


class EnergyCredits(Base):
    __tablename__ = "energy_credits"

    credit_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    billing_period_start = Column(Date, nullable=False)
    billing_period_end = Column(Date, nullable=False)
    total_generated_kwh = Column(Numeric(10, 4), nullable=True)
    total_consumed_kwh = Column(Numeric(10, 4), nullable=True)  # Fixed: Removed invalid ForeignKey
    credit_amount = Column(Numeric(10, 2), nullable=True)
    debit_amount = Column(Numeric(10, 2), nullable=True)
    net_amount = Column(Numeric(10, 2), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    customer = relationship("User", back_populates="energy_credits")

    # Composite index and check constraint
    __table_args__ = (
        Index('ix_energy_credits_customer_billing', 'customer_id', 'billing_period_start'),
        CheckConstraint('billing_period_start <= billing_period_end',
                       name='check_billing_period_dates'),
    )


class MaintenanceRecord(Base):
    __tablename__ = "maintenance_records"

    maintenance_id = Column(Integer, primary_key=True, index=True)
    panel_id = Column(Integer, ForeignKey("solar_panels.panel_id"), nullable=True)
    farm_id = Column(Integer, ForeignKey("solar_farms.farm_id"), nullable=True)
    maintenance_type = Column(String(50), nullable=True)
    scheduled_date = Column(Date, nullable=True)
    completed_date = Column(Date, nullable=True)
    description = Column(Text, nullable=True)
    # cost = Column(Numeric(10, 2), nullable=True)
    # status = Column(String(20), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    panel = relationship("SolarPanel", back_populates="maintenance_records")
    farm = relationship("SolarFarm", back_populates="maintenance_records")

    # Check constraint for maintenance dates
    __table_args__ = (
        CheckConstraint('scheduled_date IS NULL OR completed_date IS NULL OR scheduled_date <= completed_date',
                       name='check_maintenance_dates'),
    )


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

    # Relationships
    customer = relationship("User", back_populates="transactions")


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

    # Relationships
    customer = relationship("User", back_populates="notifications")
