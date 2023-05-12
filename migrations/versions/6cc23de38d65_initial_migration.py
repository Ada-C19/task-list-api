"""Initial Migration

Revision ID: 6cc23de38d65
Revises: a91689b1b85e
Create Date: 2023-05-11 16:30:36.845767

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6cc23de38d65'
down_revision = 'a91689b1b85e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('goal', sa.Column('title', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('goal', 'title')
    # ### end Alembic commands ###
