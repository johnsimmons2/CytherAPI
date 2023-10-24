"""class_to_statsheet

Revision ID: 21cc666d9b9e
Revises: 3ae500d90fce
Create Date: 2023-10-21 18:34:30.136502

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '21cc666d9b9e'
down_revision: Union[str, None] = '3ae500d90fce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
