"""empty message

Revision ID: 1087c34f32f6
Revises: b8387ea80b99
Create Date: 2018-05-02 19:35:51.197718

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1087c34f32f6'
down_revision = 'b8387ea80b99'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('random', sa.String(length=120), nullable=True))
    op.create_index(op.f('ix_user_random'), 'user', ['random'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_random'), table_name='user')
    op.drop_column('user', 'random')
    # ### end Alembic commands ###
