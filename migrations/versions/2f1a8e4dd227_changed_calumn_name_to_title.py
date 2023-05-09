"""changed calumn name to title

Revision ID: 2f1a8e4dd227
Revises: 19c159331033
Create Date: 2023-05-08 16:57:32.633316

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2f1a8e4dd227'
down_revision = '19c159331033'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('goal', sa.Column('title', sa.String(), nullable=True))
    op.drop_column('goal', 'goal_title')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('goal', sa.Column('goal_title', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('goal', 'title')
    # ### end Alembic commands ###
