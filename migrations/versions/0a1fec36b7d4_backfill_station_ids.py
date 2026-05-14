"""backfill station ids

Revision ID: 0a1fec36b7d4
Revises: 244df58d6ef4
Create Date: 2026-05-14 12:57:16.083568

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0a1fec36b7d4'
down_revision: Union[str, Sequence[str], None] = '244df58d6ef4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
    UPDATE charging_sessions_fact cs
        SET station_id = s.id
    FROM info_station s
        WHERE s.operator = cs.operator
               AND s.key = split_part(cs.evse_path, '/', 1)
               AND cs.station_id is NULL;

    """)
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
         UPDATE charging_sessions_fact 
            SET station_id = NULL;
    """)
    pass
