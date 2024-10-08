"""Adding picture under the service

Revision ID: a2f8d39cbfbf
Revises: 549fca4e50d2
Create Date: 2024-07-11 11:00:36.396353

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a2f8d39cbfbf'
down_revision = '549fca4e50d2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('services', schema=None) as batch_op:
        batch_op.add_column(sa.Column('service_image', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('services', schema=None) as batch_op:
        batch_op.drop_column('service_image')

    # ### end Alembic commands ###
