"""add column2

Revision ID: 783298317873
Revises: b8dabc3716d3
Create Date: 2024-06-29 15:21:19.043650

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '783298317873'
down_revision: Union[str, None] = 'b8dabc3716d3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('refresh_token', sa.String(length=255), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'refresh_token')
