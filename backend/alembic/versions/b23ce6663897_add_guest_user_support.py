"""add guest user support

Revision ID: b23ce6663897
Revises: 013f0140bba0
Create Date: 2024-03-19 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b23ce6663897'
down_revision = '013f0140bba0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add is_guest column to users table
    op.add_column('users', sa.Column('is_guest', sa.Boolean(), nullable=False, server_default='false'))


def downgrade() -> None:
    # Remove is_guest column from users table
    op.drop_column('users', 'is_guest')