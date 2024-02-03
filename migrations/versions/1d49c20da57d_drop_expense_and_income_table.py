"""drop expense and income table

Revision ID: 1d49c20da57d
Revises: de70a3497a86
Create Date: 2024-02-03 08:55:32.429172

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1d49c20da57d'
down_revision = 'de70a3497a86'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('expense', schema=None) as batch_op:
        batch_op.drop_index('ix_expense_account_id')
        batch_op.drop_index('ix_expense_category')
        batch_op.drop_index('ix_expense_name')

    op.drop_table('expense')
    with op.batch_alter_table('income', schema=None) as batch_op:
        batch_op.drop_index('ix_income_account_id')
        batch_op.drop_index('ix_income_category')
        batch_op.drop_index('ix_income_name')

    op.drop_table('income')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('income',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=64), autoincrement=False, nullable=False),
    sa.Column('amount', sa.NUMERIC(precision=12, scale=2), autoincrement=False, nullable=False),
    sa.Column('date_received', sa.DATE(), autoincrement=False, nullable=False),
    sa.Column('category', sa.VARCHAR(length=32), autoincrement=False, nullable=False),
    sa.Column('note', sa.VARCHAR(length=80), autoincrement=False, nullable=True),
    sa.Column('account_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['account_id'], ['account.id'], name='income_account_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='income_pkey')
    )
    with op.batch_alter_table('income', schema=None) as batch_op:
        batch_op.create_index('ix_income_name', ['name'], unique=False)
        batch_op.create_index('ix_income_category', ['category'], unique=False)
        batch_op.create_index('ix_income_account_id', ['account_id'], unique=False)

    op.create_table('expense',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=64), autoincrement=False, nullable=False),
    sa.Column('amount', sa.NUMERIC(precision=12, scale=2), autoincrement=False, nullable=False),
    sa.Column('date_spent', sa.DATE(), autoincrement=False, nullable=False),
    sa.Column('category', sa.VARCHAR(length=32), autoincrement=False, nullable=False),
    sa.Column('note', sa.VARCHAR(length=80), autoincrement=False, nullable=True),
    sa.Column('account_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['account_id'], ['account.id'], name='expense_account_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='expense_pkey')
    )
    with op.batch_alter_table('expense', schema=None) as batch_op:
        batch_op.create_index('ix_expense_name', ['name'], unique=False)
        batch_op.create_index('ix_expense_category', ['category'], unique=False)
        batch_op.create_index('ix_expense_account_id', ['account_id'], unique=False)

    # ### end Alembic commands ###
