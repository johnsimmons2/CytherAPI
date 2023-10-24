"""user_characters

Revision ID: db8f82812041
Revises: 21cc666d9b9e
Create Date: 2023-10-21 18:49:30.926203

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'db8f82812041'
down_revision: Union[str, None] = '21cc666d9b9e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
