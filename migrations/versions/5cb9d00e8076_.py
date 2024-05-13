"""empty message

Revision ID: 5cb9d00e8076
Revises: 0995a686bed0, 414072279e34
Create Date: 2024-05-13 11:45:13.921714

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5cb9d00e8076'
down_revision: Union[str, None] = ('0995a686bed0', '414072279e34')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
