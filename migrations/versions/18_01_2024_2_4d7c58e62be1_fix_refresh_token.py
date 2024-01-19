"""fix Refresh token

Revision ID: 4d7c58e62be1
Revises: 0b9c5abacfb2
Create Date: 2024-01-18 03:15:16.832306

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4d7c58e62be1'
down_revision: Union[str, None] = '0b9c5abacfb2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('refreshToken', sa.Column('jti', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('refreshToken', 'jti')
    # ### end Alembic commands ###