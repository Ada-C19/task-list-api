"""empty message

Revision ID: 22bcf2f8fb6b
Revises: 
Create Date: 2023-05-10 20:21:02.604650

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22bcf2f8fb6b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('goal',
    sa.Column('goal_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('goal_id')
    )
    op.create_table('task',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('completed_at', sa.DateTime(), nullable=True),
    sa.Column('goal_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['goal_id'], ['goal.goal_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('task')
    op.drop_table('goal')
    # ### end Alembic commands ###
