"""Added notes

Revision ID: c646da470fb7
Revises: dd9d9a67175a
Create Date: 2024-12-26 08:33:50.060016

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c646da470fb7'
down_revision: Union[str, None] = 'dd9d9a67175a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('campaign_users',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('campaignId', sa.Integer(), nullable=True),
                    sa.Column('userId', sa.Integer(), nullable=True),
                    sa.Column('active', sa.Boolean(), nullable=True),
                    sa.ForeignKeyConstraint(['campaignId'], ['campaign.id'], ),
                    sa.ForeignKeyConstraint(['userId'], ['user.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.add_column('note', sa.Column('userId', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'note', 'user', ['userId'], ['id'])
    op.add_column('note', sa.Column('characterId', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'note', 'character', ['characterId'], ['id'])
    
    op.create_table(
        'note_shared_users',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('noteId', sa.Integer(), nullable=False),
        sa.Column('userId', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['noteId'], ['note.id'], ),
        sa.ForeignKeyConstraint(['userId'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('campaign_users')
    op.add_column('note', sa.Column('campaignId', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'note', type_='foreignkey')
    op.drop_constraint(None, 'note', type_='foreignkey')
    op.drop_column('note', 'characterId')
    op.drop_column('campaign_users', 'active')
    # ### end Alembic commands ###
