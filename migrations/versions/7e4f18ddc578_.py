"""empty message

Revision ID: 7e4f18ddc578
Revises: 94687b9b964a
Create Date: 2019-01-06 11:23:20.451833

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e4f18ddc578'
down_revision = '94687b9b964a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('elimination', sa.Column('replay_id', sa.Integer(), nullable=True))
    op.drop_constraint('elimination_replay_fkey', 'elimination', type_='foreignkey')
    op.create_foreign_key(None, 'elimination', 'replay', ['replay_id'], ['id'], ondelete='CASCADE')
    op.drop_column('elimination', 'replay')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('elimination', sa.Column('replay', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'elimination', type_='foreignkey')
    op.create_foreign_key('elimination_replay_fkey', 'elimination', 'replay', ['replay'], ['id'])
    op.drop_column('elimination', 'replay_id')
    # ### end Alembic commands ###
