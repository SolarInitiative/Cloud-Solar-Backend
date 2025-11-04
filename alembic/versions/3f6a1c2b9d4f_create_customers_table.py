"""create customers table

Revision ID: 3f6a1c2b9d4f
Revises: 2607d2cf9ea0
Create Date: 2025-11-04 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3f6a1c2b9d4f'
down_revision: Union[str, Sequence[str], None] = '2607d2cf9ea0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: create customers table."""
    op.create_table(
        'customers',
        sa.Column('customer_id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('first_name', sa.String(length=100), nullable=True),
        sa.Column('last_name', sa.String(length=100), nullable=True),
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('city', sa.String(length=100), nullable=True),
        sa.Column('state', sa.String(length=100), nullable=True),
        sa.Column('postal_code', sa.String(length=20), nullable=True),
        sa.Column('utility_provider', sa.String(length=100), nullable=True),
        sa.Column('utility_account_number', sa.String(length=100), nullable=True),
        sa.Column('registration_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('account_status', sa.String(length=20), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('customer_id'),
        sa.UniqueConstraint('email', name='uq_customers_email'),
        sa.CheckConstraint("account_status IN ('Active', 'Inactive', 'Suspended')", name='ck_customers_account_status')
    )
    op.create_index(op.f('ix_customers_email'), 'customers', ['email'], unique=True)


def downgrade() -> None:
    """Downgrade schema: drop customers table."""
    op.drop_index(op.f('ix_customers_email'), table_name='customers')
    op.drop_table('customers')
