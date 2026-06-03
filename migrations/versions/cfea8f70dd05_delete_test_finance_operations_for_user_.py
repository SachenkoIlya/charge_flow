"""delete test finance operations for user 7

Revision ID: cfea8f70dd05
Revises: a3d8b23ee00f
Create Date: 2026-06-03 15:23:52.488508

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cfea8f70dd05'
down_revision: Union[str, Sequence[str], None] = 'a3d8b23ee00f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        DELETE FROM finance_operations
        WHERE user_id = 7    
    """)

def downgrade() -> None:
    pass
