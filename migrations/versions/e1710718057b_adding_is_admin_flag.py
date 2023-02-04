"""adding is admin flag

Revision ID: e1710718057b
Revises: 033597b2523c
Create Date: 2022-02-22 01:18:19.360142

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e1710718057b'
down_revision = '033597b2523c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('user', sa.Column('is_admin', sa.Boolean(), unique=False, nullable=True, default=False))

def downgrade():
    op.drop_column('user', 'is_admin')
