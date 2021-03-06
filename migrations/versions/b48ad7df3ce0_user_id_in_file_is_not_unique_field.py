"""user_id in file is not unique field

Revision ID: b48ad7df3ce0
Revises: 6c395a1900c7
Create Date: 2021-11-10 03:31:48.105352

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b48ad7df3ce0'
down_revision = '6c395a1900c7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_file_user_id', table_name='file')
    op.create_index(op.f('ix_file_user_id'), 'file', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_file_user_id'), table_name='file')
    op.create_index('ix_file_user_id', 'file', ['user_id'], unique=False)
    # ### end Alembic commands ###
