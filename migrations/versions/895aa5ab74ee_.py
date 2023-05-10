"""empty message

Revision ID: 895aa5ab74ee
Revises: 29c6c544b7b8
Create Date: 2023-05-10 11:42:06.750716

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '895aa5ab74ee'
down_revision = '29c6c544b7b8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('is_complete', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('task', 'is_complete')
    # ### end Alembic commands ###