"""added autoincrement and default arguments to Task model

Revision ID: ef7ef35dc542
Revises: 87c343550a4a
Create Date: 2023-05-04 15:19:40.405679

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef7ef35dc542'
down_revision = '87c343550a4a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, primary_key=True))
    op.drop_column('task', 'task_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('task_id', sa.INTEGER(), autoincrement=True, nullable=False))
    op.drop_column('task', 'id')
    # ### end Alembic commands ###
