"""adding refresh_token

Revision ID: 541b07b0da04
Revises: f4d3c48ddd2d
Create Date: 2024-06-29 14:20:43.781408

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '541b07b0da04'
down_revision: Union[str, None] = 'f4d3c48ddd2d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('refresh_token', sa.String(length=255), nullable=True))
    op.add_column('contacts',
                  sa.Column(
                    'user_id',
                    sa.INTEGER,
                    sa.ForeignKey("users.id",
                                  ondelete='CASCADE')
                    ))
    op.add_column('users',
                  sa.Column(
                      'avatar',
                      sa.String(length=255),
                      nullable=True
                      ))


def downgrade() -> None:
    op.drop_column('users', 'refresh_token')
    op.drop_column('contacts', 'user_id')
    op.drop_column('users', 'avatar')
