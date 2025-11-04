"""create core domain tables

Revision ID: 5c9d1e2f7b8c
Revises: 4a9b8c7d5e6f
Create Date: 2025-11-04 01:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5c9d1e2f7b8c'
down_revision: Union[str, Sequence[str], None] = '4a9b8c7d5e6f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # solar_farms
    op.create_table(
        'solar_farms',
        sa.Column('farm_id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('farm_name', sa.String(length=255), nullable=False),
        sa.Column('location_address', sa.Text(), nullable=True),
        sa.Column('latitude', sa.Numeric(10, 8), nullable=True),
        sa.Column('longitude', sa.Numeric(11, 8), nullable=True),
        sa.Column('total_capacity_kw', sa.Numeric(10, 2), nullable=True),
        sa.Column('available_capacity_kw', sa.Numeric(10, 2), nullable=True),
        sa.Column('land_lease_start_date', sa.Date(), nullable=True),
        sa.Column('land_lease_end_date', sa.Date(), nullable=True),
        sa.Column('land_owner', sa.String(length=255), nullable=True),
        sa.Column('operational_status', sa.String(length=20), nullable=True),
        sa.Column('commissioning_date', sa.Date(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # solar_panels
    op.create_table(
        'solar_panels',
        sa.Column('panel_id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('farm_id', sa.Integer(), sa.ForeignKey('solar_farms.farm_id'), nullable=True),
        sa.Column('panel_serial_number', sa.String(length=100), nullable=True),
        sa.Column('manufacturer', sa.String(length=100), nullable=True),
        sa.Column('model', sa.String(length=100), nullable=True),
        sa.Column('capacity_watts', sa.Numeric(8, 2), nullable=True),
        sa.Column('manufacture_date', sa.Date(), nullable=True),
        sa.Column('installation_date', sa.Date(), nullable=True),
        sa.Column('warranty_expiry_date', sa.Date(), nullable=True),
        sa.Column('panel_status', sa.String(length=20), nullable=True),
        sa.Column('orientation', sa.String(length=50), nullable=True),
        sa.Column('tilt_angle', sa.Numeric(5, 2), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # panel_ownership
    op.create_table(
        'panel_ownership',
        sa.Column('ownership_id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('customer_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('panel_id', sa.Integer(), sa.ForeignKey('solar_panels.panel_id'), nullable=True),
        sa.Column('ownership_type', sa.String(length=20), nullable=True),
        sa.Column('purchase_date', sa.Date(), nullable=True),
        sa.Column('purchase_price', sa.Numeric(10, 2), nullable=True),
        sa.Column('lease_start_date', sa.Date(), nullable=True),
        sa.Column('lease_end_date', sa.Date(), nullable=True),
        sa.Column('monthly_lease_amount', sa.Numeric(10, 2), nullable=True),
        sa.Column('ownership_status', sa.String(length=20), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # energy_generation
    op.create_table(
        'energy_generation',
        sa.Column('generation_id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('panel_id', sa.Integer(), sa.ForeignKey('solar_panels.panel_id'), nullable=True),
        sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False),
        sa.Column('energy_generated_kwh', sa.Numeric(10, 4), nullable=True),
        sa.Column('voltage', sa.Numeric(6, 2), nullable=True),
        sa.Column('current', sa.Numeric(6, 2), nullable=True),
        sa.Column('temperature', sa.Numeric(5, 2), nullable=True),
        sa.Column('irradiance', sa.Numeric(6, 2), nullable=True),
        sa.Column('efficiency_percentage', sa.Numeric(5, 2), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    op.create_index('idx_generation_timestamp', 'energy_generation', ['timestamp'])
    op.create_index('idx_generation_panel', 'energy_generation', ['panel_id'])

    # customer_consumption
    op.create_table(
        'customer_consumption',
        sa.Column('consumption_id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('customer_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False),
        sa.Column('energy_consumed_kwh', sa.Numeric(10, 4), nullable=True),
        sa.Column('grid_rate_per_kwh', sa.Numeric(6, 4), nullable=True),
        sa.Column('total_cost', sa.Numeric(10, 2), nullable=True),
        sa.Column('source', sa.String(length=20), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    op.create_index('idx_consumption_customer_time', 'customer_consumption', ['customer_id', 'timestamp'])

    # energy_credits
    op.create_table(
        'energy_credits',
        sa.Column('credit_id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('customer_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('billing_period_start', sa.Date(), nullable=False),
        sa.Column('billing_period_end', sa.Date(), nullable=False),
        sa.Column('total_generated_kwh', sa.Numeric(10, 4), nullable=True),
        sa.Column('total_consumed_kwh', sa.Numeric(10, 4), nullable=True),
        sa.Column('net_energy_kwh', sa.Numeric(10, 4), nullable=True),
        sa.Column('credit_amount', sa.Numeric(10, 2), nullable=True),
        sa.Column('debit_amount', sa.Numeric(10, 2), nullable=True),
        sa.Column('net_amount', sa.Numeric(10, 2), nullable=True),
        sa.Column('grid_rate_per_kwh', sa.Numeric(6, 4), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # maintenance_records
    op.create_table(
        'maintenance_records',
        sa.Column('maintenance_id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('panel_id', sa.Integer(), sa.ForeignKey('solar_panels.panel_id'), nullable=True),
        sa.Column('farm_id', sa.Integer(), sa.ForeignKey('solar_farms.farm_id'), nullable=True),
        sa.Column('maintenance_type', sa.String(length=50), nullable=True),
        sa.Column('scheduled_date', sa.Date(), nullable=True),
        sa.Column('completed_date', sa.Date(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('technician_name', sa.String(length=100), nullable=True),
        sa.Column('cost', sa.Numeric(10, 2), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # transactions
    op.create_table(
        'transactions',
        sa.Column('transaction_id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('customer_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('transaction_type', sa.String(length=30), nullable=True),
        sa.Column('amount', sa.Numeric(10, 2), nullable=True),
        sa.Column('transaction_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('payment_method', sa.String(length=50), nullable=True),
        sa.Column('payment_status', sa.String(length=20), nullable=True),
        sa.Column('reference_id', sa.String(length=100), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # inverters
    op.create_table(
        'inverters',
        sa.Column('inverter_id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('farm_id', sa.Integer(), sa.ForeignKey('solar_farms.farm_id'), nullable=True),
        sa.Column('manufacturer', sa.String(length=100), nullable=True),
        sa.Column('model', sa.String(length=100), nullable=True),
        sa.Column('serial_number', sa.String(length=100), nullable=True),
        sa.Column('max_ac_power_kw', sa.Numeric(10, 2), nullable=True),
        sa.Column('efficiency_percentage', sa.Numeric(5, 2), nullable=True),
        sa.Column('installation_date', sa.Date(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # grid_feed_in
    op.create_table(
        'grid_feed_in',
        sa.Column('feed_in_id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('farm_id', sa.Integer(), sa.ForeignKey('solar_farms.farm_id'), nullable=True),
        sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False),
        sa.Column('total_energy_fed_kwh', sa.Numeric(10, 4), nullable=True),
        sa.Column('grid_frequency', sa.Numeric(5, 2), nullable=True),
        sa.Column('voltage', sa.Numeric(6, 2), nullable=True),
        sa.Column('power_factor', sa.Numeric(4, 3), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    op.create_index('idx_grid_feed_timestamp', 'grid_feed_in', ['timestamp'])

    # notifications
    op.create_table(
        'notifications',
        sa.Column('notification_id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('customer_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('notification_type', sa.String(length=50), nullable=True),
        sa.Column('title', sa.String(length=255), nullable=True),
        sa.Column('message', sa.Text(), nullable=True),
        sa.Column('priority', sa.String(length=20), nullable=True),
        sa.Column('is_read', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('notifications')
    op.drop_index('idx_grid_feed_timestamp', table_name='grid_feed_in')
    op.drop_table('grid_feed_in')
    op.drop_table('inverters')
    op.drop_table('transactions')
    op.drop_table('maintenance_records')
    op.drop_table('energy_credits')
    op.drop_index('idx_consumption_customer_time', table_name='customer_consumption')
    op.drop_table('customer_consumption')
    op.drop_index('idx_generation_panel', table_name='energy_generation')
    op.drop_index('idx_generation_timestamp', table_name='energy_generation')
    op.drop_table('energy_generation')
    op.drop_table('panel_ownership')
    op.drop_table('solar_panels')
    op.drop_table('solar_farms')
