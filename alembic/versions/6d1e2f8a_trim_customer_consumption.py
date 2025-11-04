"""trim customer_consumption to month-level

Revision ID: 6d1e2f8a9b0c
Revises: 5c9d1e2f7b8c
Create Date: 2025-11-04 01:25:00.000000

This migration:
- Adds a `month` DATE column to `customer_consumption`.
- Backfills `month` from the existing `timestamp` by taking the month start.
- Drops unused columns: timestamp, grid_rate_per_kwh, source, created_at.
- Drops the old index on (customer_id, timestamp).

Downgrade will attempt to recreate the dropped columns (best-effort) and
repopulate timestamp from month (set to month start).
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6d1e2f8a9b0c'
down_revision: Union[str, Sequence[str], None] = '5c9d1e2f7b8c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add month column nullable initially
    op.add_column('customer_consumption', sa.Column('month', sa.Date(), nullable=True))

    # If Postgres: backfill month as date_trunc('month', timestamp)::date
    # Use a generic SQL update; this assumes PostgreSQL. If you're on another DB,
    # adjust the expression accordingly.
    op.execute(
        """
        UPDATE customer_consumption
        SET month = (date_trunc('month', timestamp))::date
        WHERE timestamp IS NOT NULL;
        """
    )

    # Drop the index on (customer_id, timestamp) if it exists
    try:
        op.drop_index('idx_consumption_customer_time', table_name='customer_consumption')
    except Exception:
        pass

    # Drop columns no longer needed
    with op.batch_alter_table('customer_consumption') as batch_op:
        try:
            batch_op.drop_column('timestamp')
        except Exception:
            pass
        try:
            batch_op.drop_column('grid_rate_per_kwh')
        except Exception:
            pass
        try:
            batch_op.drop_column('source')
        except Exception:
            pass
        try:
            batch_op.drop_column('created_at')
        except Exception:
            pass

    # Make month non-nullable now that it's populated
    with op.batch_alter_table('customer_consumption') as batch_op:
        batch_op.alter_column('month', existing_type=sa.Date(), nullable=False)


def downgrade() -> None:
    # Recreate dropped columns (best-effort)
    with op.batch_alter_table('customer_consumption') as batch_op:
        batch_op.add_column(sa.Column('timestamp', sa.DateTime(timezone=True), nullable=True))
        batch_op.add_column(sa.Column('grid_rate_per_kwh', sa.Numeric(6, 4), nullable=True))
        batch_op.add_column(sa.Column('source', sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False))

    # Populate timestamp from month (set to month start)
    op.execute(
        """
        UPDATE customer_consumption
        SET timestamp = month::timestamp
        WHERE month IS NOT NULL;
        """
    )

    # Recreate index
    op.create_index('idx_consumption_customer_time', 'customer_consumption', ['customer_id', 'timestamp'])

    # Drop the month column
    with op.batch_alter_table('customer_consumption') as batch_op:
        batch_op.drop_column('month')
