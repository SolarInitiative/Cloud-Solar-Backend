"""merge customers into users

Revision ID: 4a9b8c7d5e6f
Revises: 3f6a1c2b9d4f
Create Date: 2025-11-04 00:30:00.000000

This migration adds customer-related columns to the `users` table,
migrates data from `customers` (updating existing users and inserting
new users for customers without matching users), then drops the
`customers` table.

Note: This migration assumes a PostgreSQL backend when using
`split_part` and `now()` server_default text. Adjust if you use a
different DB.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4a9b8c7d5e6f'
down_revision: Union[str, Sequence[str], None] = '3f6a1c2b9d4f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add customer-related columns to users
    op.add_column('users', sa.Column('first_name', sa.String(length=100), nullable=True))
    op.add_column('users', sa.Column('last_name', sa.String(length=100), nullable=True))
    op.add_column('users', sa.Column('phone', sa.String(length=20), nullable=True))
    op.add_column('users', sa.Column('address', sa.Text(), nullable=True))
    op.add_column('users', sa.Column('city', sa.String(length=100), nullable=True))
    op.add_column('users', sa.Column('state', sa.String(length=100), nullable=True))
    op.add_column('users', sa.Column('postal_code', sa.String(length=20), nullable=True))
    op.add_column('users', sa.Column('utility_provider', sa.String(length=100), nullable=True))
    op.add_column('users', sa.Column('utility_account_number', sa.String(length=100), nullable=True))
    op.add_column('users', sa.Column('registration_date', sa.DateTime(timezone=True), nullable=True))
    op.add_column('users', sa.Column('account_status', sa.String(length=20), nullable=True))

    # 1) Update existing users with data from matching customers (by email)
    #    For each field we prefer the existing users value (if not null);
    #    otherwise take the customers value.
    op.execute(r"""
    UPDATE users
    SET
      first_name = COALESCE(users.first_name, c.first_name),
      last_name = COALESCE(users.last_name, c.last_name),
      phone = COALESCE(users.phone, c.phone),
      address = COALESCE(users.address, c.address),
      city = COALESCE(users.city, c.city),
      state = COALESCE(users.state, c.state),
      postal_code = COALESCE(users.postal_code, c.postal_code),
      utility_provider = COALESCE(users.utility_provider, c.utility_provider),
      utility_account_number = COALESCE(users.utility_account_number, c.utility_account_number),
      registration_date = COALESCE(users.registration_date, c.registration_date),
      account_status = COALESCE(users.account_status, c.account_status)
    FROM customers c
    WHERE users.email = c.email;
    """)

    # 2) Insert customers that don't have a matching user (by email)
    #    Use the email local-part as username. hashed_password comes
    #    from customers.password_hash. Set sensible defaults for flags.
    op.execute(r"""
    INSERT INTO users (
      username, email, hashed_password, full_name, first_name, last_name,
      phone, address, city, state, postal_code, utility_provider,
      utility_account_number, registration_date, account_status,
      created_at, updated_at, is_admin, is_active
    )
    SELECT
      -- username: local-part of the email (before @)
      split_part(c.email, '@', 1) as username,
      c.email,
      c.password_hash,
      -- full_name left NULL (users prefer full_name if present)
      NULL,
      c.first_name,
      c.last_name,
      c.phone,
      c.address,
      c.city,
      c.state,
      c.postal_code,
      c.utility_provider,
      c.utility_account_number,
      c.registration_date,
      c.account_status,
      c.created_at,
      c.updated_at,
      false,
      true
    FROM customers c
    LEFT JOIN users u ON u.email = c.email
    WHERE u.email IS NULL;
    """)

    # 3) Drop customers table (and index)
    #    remove the unique index first, if present
    try:
        op.drop_index(op.f('ix_customers_email'), table_name='customers')
    except Exception:
        # if the index does not exist, ignore
        pass
    op.drop_table('customers')


def downgrade() -> None:
    # Recreate customers table and copy back data from users for rows that
    # appear to come from customers (we select rows where any customer field
    # is non-null). This is a best-effort reversal.
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
        sa.Column('registration_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('account_status', sa.String(length=20), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint('email', name='uq_customers_email'),
        sa.CheckConstraint("account_status IN ('Active', 'Inactive', 'Suspended')", name='ck_customers_account_status')
    )

    # Copy back data from users into customers for users that appear to have
    # customer-like fields. We insert one customer row per user where
    # email is present and at least one of the customer fields is not null.
    op.execute(r"""
    INSERT INTO customers (
      email, password_hash, first_name, last_name, phone, address, city,
      state, postal_code, utility_provider, utility_account_number,
      registration_date, account_status, created_at, updated_at
    )
    SELECT
      u.email,
      u.hashed_password,
      u.first_name,
      u.last_name,
      u.phone,
      u.address,
      u.city,
      u.state,
      u.postal_code,
      u.utility_provider,
      u.utility_account_number,
      u.registration_date,
      u.account_status,
      u.created_at,
      u.updated_at
    FROM users u
    WHERE u.email IS NOT NULL
      AND (
        u.first_name IS NOT NULL OR u.last_name IS NOT NULL OR u.phone IS NOT NULL
        OR u.address IS NOT NULL OR u.utility_provider IS NOT NULL OR u.account_status IS NOT NULL
      );
    """)

    # Drop the columns we added to users
    op.drop_column('users', 'account_status')
    op.drop_column('users', 'registration_date')
    op.drop_column('users', 'utility_account_number')
    op.drop_column('users', 'utility_provider')
    op.drop_column('users', 'postal_code')
    op.drop_column('users', 'state')
    op.drop_column('users', 'city')
    op.drop_column('users', 'address')
    op.drop_column('users', 'phone')
    op.drop_column('users', 'last_name')
    op.drop_column('users', 'first_name')
