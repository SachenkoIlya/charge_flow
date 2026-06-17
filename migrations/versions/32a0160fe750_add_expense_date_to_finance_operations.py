"""add expense_date to finance_operations

Revision ID: 32a0160fe750
Revises: cfea8f70dd05
Create Date: 2026-06-17 13:08:38.554157

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '32a0160fe750'
down_revision: Union[str, Sequence[str], None] = 'cfea8f70dd05'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    op.add_column(
        "finance_operations",
        sa.Column(
            "expense_date",
            sa.Date(),
            nullable=True,
        ),
    )

    op.execute("""
        UPDATE finance_operations
        SET expense_date = created_at::date
        WHERE expense_date IS NULL
    """)

    op.alter_column(
        "finance_operations",
        "expense_date",
        nullable=False,
    )

def downgrade() -> None:
   op.drop_column(
      "finance_operations", 
      'expense_date'
   )
