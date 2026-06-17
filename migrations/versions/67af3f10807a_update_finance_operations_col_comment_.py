"""update finance_operations col comment on test

Revision ID: 67af3f10807a
Revises: 9dea8e72dcfe
Create Date: 2026-06-17 13:49:19.197712

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '67af3f10807a'
down_revision: Union[str, Sequence[str], None] = '9dea8e72dcfe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        UPDATE finance_operations
            SET comment = 'test' 
               WHERE user_id = 7
    """)

def downgrade() -> None:
    pass
