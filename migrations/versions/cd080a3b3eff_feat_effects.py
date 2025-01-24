"""feat effects

Revision ID: cd080a3b3eff
Revises: a29d4619a5a7
Create Date: 2025-01-23 22:56:47.994527

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cd080a3b3eff'
down_revision: Union[str, None] = 'a29d4619a5a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('class_feat',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('classId', sa.Integer(), nullable=False),
        sa.Column('featId', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['classId'], ['class.id'], ),
        sa.ForeignKeyConstraint(['featId'], ['feat.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('feat_effect',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('featId', sa.Integer(), nullable=False),
        sa.Column('conditionId', sa.Integer(), nullable=True),
        sa.Column('vulnerableId', sa.Integer(), nullable=True),
        sa.Column('resistantId', sa.Integer(), nullable=True),
        sa.Column('immuneId', sa.Integer(), nullable=True),
        sa.Column('abilityId', sa.Integer(), nullable=True),
        sa.Column('abilityAdj', sa.Integer(), nullable=True),
        sa.Column('skillId', sa.Integer(), nullable=True),
        sa.Column('skillAdj', sa.Integer(), nullable=True),
        sa.Column('rollAdvantage', sa.Boolean(), nullable=True),
        sa.Column('rollDisadvantage', sa.Boolean(), nullable=True),
        sa.Column('rollType', sa.String(), nullable=True),
        sa.Column('requirements', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['abilityId'], ['ability.id'], ),
        sa.ForeignKeyConstraint(['conditionId'], ['condition.id'], ),
        sa.ForeignKeyConstraint(['featId'], ['feat.id'], ),
        sa.ForeignKeyConstraint(['immuneId'], ['damage_type.id'], ),
        sa.ForeignKeyConstraint(['resistantId'], ['damage_type.id'], ),
        sa.ForeignKeyConstraint(['skillId'], ['skill.id'], ),
        sa.ForeignKeyConstraint(['vulnerableId'], ['damage_type.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.add_column('condition_effect', sa.Column('description', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('condition_effect', 'description')
    op.drop_table('feat_effect')
    op.drop_table('class_feat')
    # ### end Alembic commands ###
