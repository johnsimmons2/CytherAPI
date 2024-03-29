"""remove subclassid

Revision ID: dbb78926edf0
Revises: f656e8870684
Create Date: 2024-01-21 18:30:43.862533

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dbb78926edf0'
down_revision: Union[str, None] = 'f656e8870684'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint('subclass_classId_fkey', 'subclass', type_='foreignkey')
    op.drop_column('subclass', 'classId')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('subclass', sa.Column('classId', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('subclass_classId_fkey', 'subclass', 'class', ['classId'], ['id'])
    # ### end Alembic commands ###
