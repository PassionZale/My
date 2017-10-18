"""empty message

Revision ID: a601cdb6c045
Revises: 038cab0ed6a9
Create Date: 2017-09-27 23:44:09.058571

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a601cdb6c045'
down_revision = '038cab0ed6a9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('flasky_articles', sa.Column('test', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('flasky_articles', 'test')
    # ### end Alembic commands ###
