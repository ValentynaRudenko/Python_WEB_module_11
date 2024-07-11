"""token

Revision ID: 9d5bc663e2b5
Revises: 3b811df1dcef
Create Date: 2024-06-30 20:24:55.109508

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9d5bc663e2b5'
down_revision: Union[str, None] = '3b811df1dcef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# def upgrade() -> None:
#     op.add_column('users', sa.Column('refresh_token', sa.String(length=255), nullable=True))


# def downgrade() -> None:
#     op.drop_column('users', 'refresh_token')

def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
