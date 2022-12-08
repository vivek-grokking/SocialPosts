"""add remaining cols to posts table

Revision ID: 22ff6b7d520d
Revises: 2bc6c7448453
Create Date: 2022-12-08 17:27:37.995375

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22ff6b7d520d'
down_revision = '2bc6c7448453'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(),
                  nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                                     server_default=sa.text('now()'), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
