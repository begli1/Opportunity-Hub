"""upgrade moderation_link_opens schema

Revision ID: upgrade_mod_links
Revises: add_mod_link_opens
Create Date: Safe link review - action, normalized_url, host, risk_level, reasons, logging

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'upgrade_mod_links'
down_revision: Union[str, Sequence[str], None] = 'add_mod_link_opens'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('moderation_link_opens', sa.Column('action', sa.String(length=20), nullable=True))
    op.add_column('moderation_link_opens', sa.Column('normalized_url', sa.String(length=2048), nullable=True))
    op.add_column('moderation_link_opens', sa.Column('host', sa.String(length=253), nullable=True))
    op.add_column('moderation_link_opens', sa.Column('risk_level', sa.String(length=10), nullable=True))
    op.add_column('moderation_link_opens', sa.Column('reasons', sa.Text(), nullable=True))
    op.add_column('moderation_link_opens', sa.Column('user_agent', sa.String(length=500), nullable=True))
    op.add_column('moderation_link_opens', sa.Column('ip', sa.String(length=45), nullable=True))
    op.add_column('moderation_link_opens', sa.Column('created_at', sa.DateTime(timezone=True), nullable=True))

    # Backfill existing rows
    op.execute("""
        UPDATE moderation_link_opens
        SET action = 'OPEN',
            normalized_url = url,
            host = '',
            risk_level = 'LOW',
            created_at = opened_at
        WHERE normalized_url IS NULL
    """)

    op.drop_column('moderation_link_opens', 'opened_at')
    op.drop_column('moderation_link_opens', 'url')

    op.alter_column('moderation_link_opens', 'action', nullable=False)
    op.alter_column('moderation_link_opens', 'normalized_url', nullable=False)
    op.alter_column('moderation_link_opens', 'host', nullable=False)
    op.alter_column('moderation_link_opens', 'risk_level', nullable=False)
    op.alter_column('moderation_link_opens', 'created_at', nullable=False)


def downgrade() -> None:
    op.add_column('moderation_link_opens', sa.Column('url', sa.String(length=500), nullable=True))
    op.add_column('moderation_link_opens', sa.Column('opened_at', sa.DateTime(timezone=True), nullable=True))
    op.execute("UPDATE moderation_link_opens SET url = normalized_url, opened_at = created_at")
    op.alter_column('moderation_link_opens', 'url', nullable=False)
    op.alter_column('moderation_link_opens', 'opened_at', nullable=False)
    op.drop_column('moderation_link_opens', 'created_at')
    op.drop_column('moderation_link_opens', 'ip')
    op.drop_column('moderation_link_opens', 'user_agent')
    op.drop_column('moderation_link_opens', 'reasons')
    op.drop_column('moderation_link_opens', 'risk_level')
    op.drop_column('moderation_link_opens', 'host')
    op.drop_column('moderation_link_opens', 'normalized_url')
    op.drop_column('moderation_link_opens', 'action')
