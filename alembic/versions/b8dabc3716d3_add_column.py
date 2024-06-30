"""add column

Revision ID: b8dabc3716d3
Revises: 541b07b0da04
Create Date: 2024-06-29 15:18:58.227162

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b8dabc3716d3'
down_revision: Union[str, None] = '541b07b0da04'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
