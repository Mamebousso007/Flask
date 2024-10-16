"""empty message

Revision ID: 68f2578e6724
Revises: 1c4516f1e063
Create Date: 2024-10-11 17:50:44.475205

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '68f2578e6724'
down_revision = '1c4516f1e063'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('role',
               existing_type=postgresql.ENUM('ADMIN', 'USER', name='roleenum'),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('role',
               existing_type=postgresql.ENUM('ADMIN', 'USER', name='roleenum'),
               nullable=True)

    # ### end Alembic commands ###
