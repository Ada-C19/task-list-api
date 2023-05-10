"""empty message

Revision ID: 675e5e888ee6
Revises: 908be9744d8e
Create Date: 2023-05-09 21:43:59.024597

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '675e5e888ee6'
down_revision = '908be9744d8e'
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
