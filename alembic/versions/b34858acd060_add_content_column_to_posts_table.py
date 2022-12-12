"""add content column to posts table

Revision ID: b34858acd060
Revises: 1dc9048fc864
Create Date: 2022-12-08 16:29:28.364698

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b34858acd060'
down_revision = '1dc9048fc864'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
