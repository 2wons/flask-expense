"""budget table

Revision ID: e5d356989b5a
Revises: 1d49c20da57d
Create Date: 2024-02-07 22:53:51.924633

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5d356989b5a'
down_revision = '1d49c20da57d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('budget',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.Column('month', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Numeric(precision=12, scale=2), nullable=False),
    sa.Column('limits_dict', sa.JSON(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('budget', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_budget_month'), ['month'], unique=False)
        batch_op.create_index(batch_op.f('ix_budget_user_id'), ['user_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_budget_year'), ['year'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('budget', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_budget_year'))
        batch_op.drop_index(batch_op.f('ix_budget_user_id'))
        batch_op.drop_index(batch_op.f('ix_budget_month'))

    op.drop_table('budget')
    # ### end Alembic commands ###