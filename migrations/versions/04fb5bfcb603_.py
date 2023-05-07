"""empty message

Revision ID: 04fb5bfcb603
Revises: 1991978cb704
Create Date: 2023-05-06 17:03:21.392474

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04fb5bfcb603'
down_revision = '1991978cb704'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('goal_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'task', 'goal', ['goal_id'], ['goal_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'task', type_='foreignkey')
    op.drop_column('task', 'goal_id')
    # ### end Alembic commands ###
