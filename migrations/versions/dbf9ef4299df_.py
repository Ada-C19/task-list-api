"""empty message

Revision ID: dbf9ef4299df
Revises: 6814d791c284
Create Date: 2023-05-09 13:54:19.174133

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dbf9ef4299df'
down_revision = '6814d791c284'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('id', sa.Integer(), nullable=False))
    op.drop_column('task', 'task_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('task_id', sa.INTEGER(), autoincrement=True, nullable=False))
    op.drop_column('task', 'id')
    # ### end Alembic commands ###