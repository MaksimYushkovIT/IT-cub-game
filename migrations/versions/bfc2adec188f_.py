"""empty message

Revision ID: bfc2adec188f
Revises: ea9a3e4e47ba
Create Date: 2024-09-29 21:58:00.296996

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bfc2adec188f'
down_revision = 'ea9a3e4e47ba'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('discipline_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'disciplines', ['discipline_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('discipline_id')

    # ### end Alembic commands ###
