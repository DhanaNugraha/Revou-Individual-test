"""feat: removed stuff from product

Revision ID: 97ad1530a22d
Revises: 5f02875b0561
Create Date: 2025-04-17 20:57:23.608438

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97ad1530a22d'
down_revision = '5f02875b0561'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.drop_column('production_location')
        batch_op.drop_column('is_organic')
        batch_op.drop_column('is_locally_produced')
        batch_op.drop_column('carbon_footprint')
        batch_op.drop_column('unit_type')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.add_column(sa.Column('unit_type', sa.VARCHAR(length=20), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('carbon_footprint', sa.NUMERIC(precision=10, scale=2), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('is_locally_produced', sa.BOOLEAN(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('is_organic', sa.BOOLEAN(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('production_location', sa.VARCHAR(length=100), autoincrement=False, nullable=True))

    # ### end Alembic commands ###
