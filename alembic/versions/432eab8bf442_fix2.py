"""Fix2

Revision ID: 432eab8bf442
Revises: b6c5eeb72196
Create Date: 2024-06-30 19:14:49.852854

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '432eab8bf442'
down_revision: Union[str, None] = 'b6c5eeb72196'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Add user_id column with a default value
    op.add_column('contacts', sa.Column('user_id', sa.Integer(), nullable=True, server_default='1'))

    # Update the column to set NOT NULL after setting the default
    op.alter_column('contacts', 'user_id', existing_type=sa.Integer(), nullable=False, server_default=None)


def downgrade():
    # Drop user_id column
    op.drop_column('contacts', 'user_id')
