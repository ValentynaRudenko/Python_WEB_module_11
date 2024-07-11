"""Allow NULL values for user_id temporarily

Revision ID: e1e1d8d7d9fc
Revises: 432eab8bf442
Create Date: 2024-06-30 19:24:42.171396

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e1e1d8d7d9fc'
down_revision: Union[str, None] = '432eab8bf442'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# def upgrade():
#     # Allow NULL values for user_id column temporarily
#     op.alter_column('contacts', 'user_id', existing_type=sa.Integer(), nullable=True)


# def downgrade():
#     # Revert back to NOT NULL constraint if downgrading
#     op.alter_column('contacts', 'user_id', existing_type=sa.Integer(), nullable=False)


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
