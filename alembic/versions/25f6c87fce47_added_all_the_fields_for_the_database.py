"""added all the fields for the dataBase

Revision ID: 25f6c87fce47
Revises: 5c9d1e2f7b8c
Create Date: 2025-11-04 18:42:12.267617

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '25f6c87fce47'
down_revision: Union[str, Sequence[str], None] = '5c9d1e2f7b8c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
