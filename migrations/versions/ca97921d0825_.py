"""empty message

Revision ID: ca97921d0825
Revises: 
Create Date: 2022-05-11 21:27:44.759956

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca97921d0825'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('score', sa.Column('something', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('score', 'something')
    # ### end Alembic commands ###