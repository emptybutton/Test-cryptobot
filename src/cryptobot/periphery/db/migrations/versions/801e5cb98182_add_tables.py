"""add tables

Revision ID: 801e5cb98182
Revises: 
Create Date: 2024-07-10 09:25:13.795017

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '801e5cb98182'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cryptocurrencies',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('symbol', sa.String(), nullable=False),
    sa.Column('in_dollars', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('telegram_chat_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('trackings',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('cryptocurrency_id', sa.String(), nullable=False),
    sa.Column('lower_threshold_dollars', sa.Integer(), nullable=False),
    sa.Column('upper_threshold_dollars', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['cryptocurrency_id'], ['cryptocurrencies.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('trackings')
    op.drop_table('users')
    op.drop_table('cryptocurrencies')
    # ### end Alembic commands ###
