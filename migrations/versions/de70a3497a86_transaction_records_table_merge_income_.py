"""Transaction records table (merge income and expense)

Revision ID: de70a3497a86
Revises: fc81b9247233
Create Date: 2024-02-01 23:56:13.106395

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de70a3497a86'
down_revision = 'fc81b9247233'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('record',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('amount', sa.Numeric(precision=12, scale=2), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('category', sa.String(length=32), nullable=False),
    sa.Column('type', sa.String(length=16), nullable=False),
    sa.Column('note', sa.String(length=80), nullable=True),
    sa.Column('account_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['account_id'], ['account.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('record', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_record_account_id'), ['account_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_record_category'), ['category'], unique=False)
        batch_op.create_index(batch_op.f('ix_record_name'), ['name'], unique=False)
        batch_op.create_index(batch_op.f('ix_record_type'), ['type'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('record', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_record_type'))
        batch_op.drop_index(batch_op.f('ix_record_name'))
        batch_op.drop_index(batch_op.f('ix_record_category'))
        batch_op.drop_index(batch_op.f('ix_record_account_id'))

    op.drop_table('record')
    # ### end Alembic commands ###