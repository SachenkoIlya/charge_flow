"""add mode column to finance operations

Revision ID: a3d8b23ee00f
Revises: 5f88864b5033
Create Date: 2026-06-02 15:49:07.327448

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a3d8b23ee00f'
down_revision: Union[str, Sequence[str], None] = '5f88864b5033'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'finance_operations',
        sa.Column(
            'mode', 
            sa.String(length=20), 
            nullable=False, 
            server_default='opex'
        )
    )


def downgrade() -> None:
    op.drop_column('finance_operations', 'mode')