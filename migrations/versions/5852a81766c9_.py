"""empty message

Revision ID: 5852a81766c9
Revises: d3a04899ce94
Create Date: 2023-05-07 17:46:11.773698

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5852a81766c9'
down_revision = 'd3a04899ce94'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('goal',
    sa.Column('goal_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('goal_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('goal')
    # ### end Alembic commands ###