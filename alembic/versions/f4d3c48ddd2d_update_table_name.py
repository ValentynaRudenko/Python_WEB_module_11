"""update table name

Revision ID: f4d3c48ddd2d
Revises: 7d131a831ddb
Create Date: 2024-06-24 21:51:43.784200

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f4d3c48ddd2d'
down_revision: Union[str, None] = '7d131a831ddb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
