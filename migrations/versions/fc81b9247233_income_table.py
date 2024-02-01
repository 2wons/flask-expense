"""income table

Revision ID: fc81b9247233
Revises: 2588269bdd1a
Create Date: 2024-02-01 10:14:07.116455

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc81b9247233'
down_revision = '2588269bdd1a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('income',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('amount', sa.Numeric(precision=12, scale=2), nullable=False),
    sa.Column('date_received', sa.Date(), nullable=False),
    sa.Column('category', sa.String(length=32), nullable=False),
    sa.Column('note', sa.String(length=80), nullable=True),
    sa.Column('account_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['account_id'], ['account.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('income', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_income_account_id'), ['account_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_income_category'), ['category'], unique=False)
        batch_op.create_index(batch_op.f('ix_income_name'), ['name'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('income', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_income_name'))
        batch_op.drop_index(batch_op.f('ix_income_category'))
        batch_op.drop_index(batch_op.f('ix_income_account_id'))

    op.drop_table('income')
    # ### end Alembic commands ###
