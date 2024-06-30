"""add user relations

Revision ID: 4c75966c51e9
Revises: 783298317873
Create Date: 2024-06-30 14:36:35.537237

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4c75966c51e9'
down_revision: Union[str, None] = '783298317873'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
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
    op.drop_column('contacts', 'user_id')
    op.drop_column('users', 'avatar')
