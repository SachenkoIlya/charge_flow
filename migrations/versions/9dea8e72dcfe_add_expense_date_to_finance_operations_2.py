"""add expense_date to finance_operations 2

Revision ID: 9dea8e72dcfe
Revises: 9465965bc1ce
Create Date: 2026-06-17 13:40:05.730347

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9dea8e72dcfe'
down_revision: Union[str, Sequence[str], None] = '9465965bc1ce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
