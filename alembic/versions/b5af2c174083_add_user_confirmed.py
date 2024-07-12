"""add User / confirmed

Revision ID: b5af2c174083
Revises: 9d5bc663e2b5
Create Date: 2024-07-07 13:48:03.956129

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b5af2c174083'
down_revision: Union[str, None] = '9d5bc663e2b5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('confirmed', sa.Boolean, default=False))


def downgrade() -> None:
    op.drop_column('users', 'confirmed')
