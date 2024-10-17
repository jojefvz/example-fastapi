"""add content column to posts table

Revision ID: 7a9eec8d115e
Revises: 32a3a876dd9c
Create Date: 2024-10-16 19:13:51.824628

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7a9eec8d115e'
down_revision: Union[str, None] = '32a3a876dd9c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
