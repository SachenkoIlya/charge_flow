"""add completed station metrics index

Revision ID: 244df58d6ef4
Revises: 99245df8540b
Create Date: 2026-05-14 12:27:03.872073

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '244df58d6ef4'
down_revision: Union[str, Sequence[str], None] = '99245df8540b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
    CREATE INDEX idx_completed_user_station_start_ts ON 
        charging_sessions_fact(user_id, station_id, start_ts)
        WHERE state IN ('COMPLETED', 'CHARGED');             
    """)
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
        DROP INDEX idx_completed_user_station_start_ts;
    """)
    pass
