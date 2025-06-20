"""Modified Templates model

Revision ID: 4104876f2796
Revises: b8397413041d
Create Date: 2025-05-22 22:43:19.586563

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4104876f2796'
down_revision = 'b8397413041d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('templates', sa.Column('description', sa.Text(), nullable=True))
    op.add_column('templates', sa.Column('content', sa.Text(), nullable=True))
    op.add_column('templates', sa.Column('data', sa.JSON(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('templates', 'data')
    op.drop_column('templates', 'content')
    op.drop_column('templates', 'description')
    # ### end Alembic commands ###