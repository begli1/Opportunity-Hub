"""add moderation_link_opens

Revision ID: add_mod_link_opens
Revises: 2876931582b8
Create Date: Safe external link review logging

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'add_mod_link_opens'
down_revision: Union[str, Sequence[str], None] = '2876931582b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'moderation_link_opens',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('opportunity_id', sa.Integer(), nullable=False),
        sa.Column('moderator_user_id', sa.Integer(), nullable=False),
        sa.Column('url', sa.String(length=500), nullable=False),
        sa.Column('opened_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['opportunity_id'], ['opportunities.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['moderator_user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    with op.batch_alter_table('moderation_link_opens', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_moderation_link_opens_opportunity_id'), ['opportunity_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_moderation_link_opens_moderator_user_id'), ['moderator_user_id'], unique=False)


def downgrade() -> None:
    with op.batch_alter_table('moderation_link_opens', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_moderation_link_opens_moderator_user_id'))
        batch_op.drop_index(batch_op.f('ix_moderation_link_opens_opportunity_id'))
    op.drop_table('moderation_link_opens')
