"""create db

Revision ID: a1316b7b88ae
Revises: 
Create Date: 2019-06-06 20:07:47.074558

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1316b7b88ae'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('firstname', sa.String(length=32), nullable=False),
    sa.Column('lastname', sa.String(length=32), nullable=False),
    sa.Column('username', sa.String(length=32), nullable=False),
    sa.Column('email', sa.String(length=128), nullable=False),
    sa.Column('pwhash', sa.String(length=128), nullable=True),
    sa.Column('institution', sa.String(length=120), nullable=False),
    sa.Column('department', sa.String(length=64), nullable=False),
    sa.Column('programme', sa.String(length=64), nullable=False),
    sa.Column('registered_on', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('project',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=128), nullable=False),
    sa.Column('authors', sa.Text(), nullable=False),
    sa.Column('submit_date', sa.DateTime(), nullable=False),
    sa.Column('file_data', sa.LargeBinary(), nullable=True),
    sa.Column('filename', sa.String(length=120), nullable=False),
    sa.Column('modified_at', sa.DateTime(), nullable=True),
    sa.Column('owner', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['owner'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('filename')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('project')
    op.drop_table('user')
    # ### end Alembic commands ###
