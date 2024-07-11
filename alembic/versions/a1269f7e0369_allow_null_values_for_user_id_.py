"""Allow NULL values for user_id temporarily

Revision ID: a1269f7e0369
Revises: df6e115b9291
Create Date: 2024-06-30 19:50:36.847423

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1269f7e0369'
down_revision: Union[str, None] = 'df6e115b9291'
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
