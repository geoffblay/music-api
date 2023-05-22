"""updating weather table, adding column

Revision ID: f6a0769cb6fb
Revises: 
Create Date: 2023-05-21 21:08:08.839811

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f6a0769cb6fb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('genres',
    sa.Column('genre_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('genre_id')
    )
    op.create_table('vibe',
    sa.Column('vibe_id', sa.Integer(), nullable=False),
    sa.Column('vibe', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('vibe_id')
    )
    op.create_table('weather',
    sa.Column('weather_id', sa.Integer(), nullable=False),
    sa.Column('weather', sa.Text(), nullable=False),
    sa.Column('weather_rating', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('weather_id')
    )
    op.drop_table('subgenres')
    op.add_column('albums', sa.Column('genre_id', sa.Integer(), nullable=False))
    op.drop_constraint('albums_subgenre_id_fkey', 'albums', type_='foreignkey')
    op.create_foreign_key(None, 'albums', 'genres', ['genre_id'], ['genre_id'])
    op.drop_column('albums', 'subgenre_id')
    op.alter_column('artists', 'gender',
               existing_type=sa.VARCHAR(length=160),
               nullable=True)
    op.add_column('tracks', sa.Column('genre_id', sa.Integer(), nullable=False))
    op.add_column('tracks', sa.Column('weather_id', sa.Integer(), nullable=False))
    op.drop_constraint('tracks_subgenre_id_fkey', 'tracks', type_='foreignkey')
    op.create_foreign_key(None, 'tracks', 'genres', ['genre_id'], ['genre_id'])
    op.create_foreign_key(None, 'tracks', 'weather', ['weather_id'], ['weather_id'])
    op.drop_column('tracks', 'subgenre_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tracks', sa.Column('subgenre_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'tracks', type_='foreignkey')
    op.drop_constraint(None, 'tracks', type_='foreignkey')
    op.create_foreign_key('tracks_subgenre_id_fkey', 'tracks', 'subgenres', ['subgenre_id'], ['subgenre_id'])
    op.drop_column('tracks', 'weather_id')
    op.drop_column('tracks', 'genre_id')
    op.alter_column('artists', 'gender',
               existing_type=sa.VARCHAR(length=160),
               nullable=False)
    op.add_column('albums', sa.Column('subgenre_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'albums', type_='foreignkey')
    op.create_foreign_key('albums_subgenre_id_fkey', 'albums', 'subgenres', ['subgenre_id'], ['subgenre_id'])
    op.drop_column('albums', 'genre_id')
    op.create_table('subgenres',
    sa.Column('subgenre_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=160), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('subgenre_id', name='subgenres_pkey')
    )
    op.drop_table('weather')
    op.drop_table('vibe')
    op.drop_table('genres')
    # ### end Alembic commands ###
