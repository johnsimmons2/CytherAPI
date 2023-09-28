"""init

Revision ID: cc869b12d7da
Revises: 
Create Date: 2023-09-01 17:55:25.132296

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cc869b12d7da'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('class',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('inventory',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('itemId', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('items',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('type', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('role',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('roleName', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('spellbook',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('spellslot1', sa.Integer(), nullable=True),
    sa.Column('spellslot2', sa.Integer(), nullable=True),
    sa.Column('spellslot3', sa.Integer(), nullable=True),
    sa.Column('spellslot4', sa.Integer(), nullable=True),
    sa.Column('spellslot5', sa.Integer(), nullable=True),
    sa.Column('spellslot6', sa.Integer(), nullable=True),
    sa.Column('spellslot7', sa.Integer(), nullable=True),
    sa.Column('spellslot8', sa.Integer(), nullable=True),
    sa.Column('spellslot9', sa.Integer(), nullable=True),
    sa.Column('warlockslots', sa.Integer(), nullable=True),
    sa.Column('warlockslotlevel', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('spellcomponents',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('spellId', sa.Integer(), nullable=True),
    sa.Column('itemId', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('goldValue', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('spells',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('spellComponentId', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('castingTime', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('duration', sa.String(), nullable=True),
    sa.Column('school', sa.String(), nullable=True),
    sa.Column('type', sa.Integer(), nullable=True),
    sa.Column('level', sa.Integer(), nullable=True),
    sa.Column('verbal', sa.Boolean(), nullable=True),
    sa.Column('somatic', sa.Boolean(), nullable=True),
    sa.Column('material', sa.Boolean(), nullable=True),
    sa.Column('ritual', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('subclass',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('classId', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('fName', sa.String(), nullable=True),
    sa.Column('lName', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('salt', sa.String(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('lastOnline', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('cantripknowledge',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('spellbookId', sa.Integer(), nullable=True),
    sa.Column('spellId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['spellbookId'], ['spellbook.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('character',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('userId', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('type', sa.Integer(), nullable=True),
    sa.Column('race', sa.String(), nullable=True),
    sa.Column('className', sa.String(), nullable=True),
    sa.Column('subClassName', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['userId'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('spellbookknowledge',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('spellbookId', sa.Integer(), nullable=True),
    sa.Column('spellId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['spellbookId'], ['spellbook.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('spellbookprepared',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('spellbookId', sa.Integer(), nullable=True),
    sa.Column('spellId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['spellbookId'], ['spellbook.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_role',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('userId', sa.Integer(), nullable=True),
    sa.Column('roleId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['roleId'], ['role.id'], ),
    sa.ForeignKeyConstraint(['userId'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('statsheet',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('characterId', sa.Integer(), nullable=True),
    sa.Column('spellbookId', sa.Integer(), nullable=True),
    sa.Column('strength', sa.Integer(), nullable=True),
    sa.Column('dexterity', sa.Integer(), nullable=True),
    sa.Column('constitution', sa.Integer(), nullable=True),
    sa.Column('intelligence', sa.Integer(), nullable=True),
    sa.Column('wisdom', sa.Integer(), nullable=True),
    sa.Column('charisma', sa.Integer(), nullable=True),
    sa.Column('health', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['characterId'], ['character.id'], ),
    sa.ForeignKeyConstraint(['spellbookId'], ['spellbook.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('characterId'),
    sa.UniqueConstraint('spellbookId')
    )
    op.create_table('hitdice',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('statsheetId', sa.Integer(), nullable=True),
    sa.Column('d6', sa.Integer(), nullable=True),
    sa.Column('d8', sa.Integer(), nullable=True),
    sa.Column('d10', sa.Integer(), nullable=True),
    sa.Column('d12', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['statsheetId'], ['statsheet.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('hitdice')
    op.drop_table('statsheet')
    op.drop_table('user_role')
    op.drop_table('spellbookprepared')
    op.drop_table('spellbookknowledge')
    op.drop_table('character')
    op.drop_table('cantripknowledge')
    op.drop_table('user')
    op.drop_table('subclass')
    op.drop_table('spells')
    op.drop_table('spellcomponents')
    op.drop_table('spellbook')
    op.drop_table('role')
    op.drop_table('items')
    op.drop_table('inventory')
    op.drop_table('class')
    # ### end Alembic commands ###
