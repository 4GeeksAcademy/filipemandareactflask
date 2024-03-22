"""empty message

Revision ID: 583c83e450f7
Revises: 64245dd58a29
Create Date: 2024-03-22 14:38:45.307613

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '583c83e450f7'
down_revision = '64245dd58a29'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('todolist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('task', sa.String(length=120), nullable=False),
    sa.Column('done', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('task')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('todolist')
    # ### end Alembic commands ###