"""modified task table string length is 255

Revision ID: 8208e8186ede
Revises: 2260413c2b8e
Create Date: 2023-05-14 11:46:43.700793

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8208e8186ede'
down_revision = '2260413c2b8e'
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
