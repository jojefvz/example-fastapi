"""add foreign key to posts table

Revision ID: 691b5b0aebaa
Revises: 93e75b1fd667
Create Date: 2024-10-16 19:40:17.788897

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '691b5b0aebaa'
down_revision: Union[str, None] = '93e75b1fd667'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer, nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts', 
                          referent_table='users', local_cols=['owner_id'], 
                          remote_cols=['id'], ondelete='CASCADE'
                          )


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
