"""Established one to many relationship, one goal, many tasks

Revision ID: 08c7252f8eed
Revises: da58fc4f2f7c
Create Date: 2023-05-10 08:25:24.503958

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '08c7252f8eed'
down_revision = 'da58fc4f2f7c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('goal', sa.Column('title', sa.String(), nullable=True))
    op.add_column('task', sa.Column('goal_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'task', 'goal', ['goal_id'], ['goal_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'task', type_='foreignkey')
    op.drop_column('task', 'goal_id')
    op.drop_column('goal', 'title')
    # ### end Alembic commands ###
