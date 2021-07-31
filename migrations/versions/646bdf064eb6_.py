"""empty message

Revision ID: 646bdf064eb6
Revises: 
Create Date: 2021-07-31 17:22:02.235408

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '646bdf064eb6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('movies_actiors_worked_in')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('movies_actiors_worked_in',
    sa.Column('movie_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('actor_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['actor_id'], ['actors.id'], name='movies_actiors_worked_in_actor_id_fkey'),
    sa.ForeignKeyConstraint(['movie_id'], ['movies.id'], name='movies_actiors_worked_in_movie_id_fkey'),
    sa.PrimaryKeyConstraint('movie_id', 'actor_id', name='movies_actiors_worked_in_pkey')
    )
    # ### end Alembic commands ###