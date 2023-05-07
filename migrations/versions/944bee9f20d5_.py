"""empty message

Revision ID: 944bee9f20d5
Revises: 3ffd5e80b180
Create Date: 2023-05-07 10:39:37.976461

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '944bee9f20d5'
down_revision = '3ffd5e80b180'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('goal', sa.Column('id', sa.Integer(), autoincrement=True, nullable=False))
    op.drop_column('goal', 'goal_id')
    op.add_column('task', sa.Column('goal_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'task', 'goal', ['goal_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'task', type_='foreignkey')
    op.drop_column('task', 'goal_id')
    op.add_column('goal', sa.Column('goal_id', sa.INTEGER(), autoincrement=True, nullable=False))
    op.drop_column('goal', 'id')
    # ### end Alembic commands ###
