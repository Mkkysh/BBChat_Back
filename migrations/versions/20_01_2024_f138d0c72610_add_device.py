"""add device

Revision ID: f138d0c72610
Revises: 19cfc323707a
Create Date: 2024-01-20 00:58:55.336099

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f138d0c72610'
down_revision: Union[str, None] = '19cfc323707a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('refreshToken', sa.Column('user_agent', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('refreshToken', 'user_agent')
    # ### end Alembic commands ###
