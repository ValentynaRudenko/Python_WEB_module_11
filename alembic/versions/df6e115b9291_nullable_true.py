"""Nullable true

Revision ID: df6e115b9291
Revises: e1e1d8d7d9fc
Create Date: 2024-06-30 19:30:50.732037

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'df6e115b9291'
down_revision: Union[str, None] = 'e1e1d8d7d9fc'
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
