"""Version_3

Revision ID: 724b8cb1bb40
Revises: 8072f6720544
Create Date: 2024-06-03 23:47:15.856050

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '724b8cb1bb40'
down_revision: Union[str, None] = '8072f6720544'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contacts', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'contacts', 'users', ['user_id'], ['id'])
    op.add_column('users', sa.Column('avatar', sa.String(length=255), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'avatar')
    op.drop_constraint(None, 'contacts', type_='foreignkey')
    op.drop_column('contacts', 'user_id')
    # ### end Alembic commands ###
