"""ext-table

Revision ID: 43a571f53c03
Revises: db8f82812041
Create Date: 2023-12-30 16:41:18.599467

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '43a571f53c03'
down_revision: Union[str, None] = 'db8f82812041'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
