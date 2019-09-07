"""
Create feedeater tables (feed, article, feed_result)

Revision ID: b3a7e2b375e0
Revises: 0001c8ac1a69
Create Date: 2018-12-23 15:04:57.578448

"""

# revision identifiers, used by Alembic.
revision = 'b3a7e2b375e0'
down_revision = '0001c8ac1a69'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


def upgrade():
    op.create_table('feed',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('status', sa.Integer(), server_default='1', nullable=False),
        sa.Column('url', sa.String(length=200), nullable=False),
        sa.Column('title', sa.String(length=100), nullable=False),
        sa.Column('type', sa.String(length=10), nullable=False),
        sa.Column('htmlUrl', sa.String(length=200), nullable=True),
        sa.Column('etag', sa.String(length=200), nullable=True),
        sa.Column('updated', sa.DateTime(), nullable=True),
        sa.Column('created', sa.DateTime(), nullable=False),
        sa.Column('fetched', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('article',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('article_id', sa.String(length=200), nullable=False),
        sa.Column('title', sa.String(length=500), nullable=True),
        sa.Column('published', sa.DateTime(), nullable=True),
        sa.Column('summary', sa.Text(), nullable=True),
        sa.Column('link', sa.String(length=300), nullable=True),
        sa.Column('fetched', sa.DateTime(), nullable=False),
        sa.Column('feed_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['feed_id'], ['feed.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('feed_result',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('status_code', sa.Integer(), nullable=True),
        sa.Column('completed_date', sa.DateTime(), nullable=False),
        sa.Column('log', sa.JSON(), nullable=True),
        sa.Column('had_exception', sa.Boolean(), nullable=False),
        sa.Column('feed_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['feed_id'], ['feed.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('feed_result')
    op.drop_table('article')
    op.drop_table('feed')
