"""repeat add column

Revision ID: 3b811df1dcef
Revises: a1269f7e0369
Create Date: 2024-06-30 19:55:05.692832

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3b811df1dcef'
down_revision: Union[str, None] = 'a1269f7e0369'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# def upgrade():
#     op.add_column('contacts',
#                   sa.Column(
#                     'user_id',
#                     sa.INTEGER,
#                     sa.ForeignKey("users.id",
#                                   ondelete='CASCADE'),
#                     nullable=True
#                     ))
#     op.add_column('users',
#                   sa.Column(
#                       'avatar',
#                       sa.String(length=255),
#                       nullable=True
#                       ))


# def downgrade():
#     op.drop_column('contacts', 'user_id')
#     op.drop_column('users', 'avatar')


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
