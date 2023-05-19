"""testing alembic on prod

Revision ID: f93b8aa19ccf
Revises: 
Create Date: 2023-05-18 18:06:53.572592

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f93b8aa19ccf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('artists',
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('gender', sa.Text(), nullable=True),
    sa.Column('deathdate', sa.Date(), nullable=True),
    sa.Column('birthdate', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('artist_id')
    )
    op.create_table('genres',
    sa.Column('genre_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('genre_id')
    )
    op.create_table('playlists',
    sa.Column('playlist_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('playlist_id')
    )
    op.create_table('vibe',
    sa.Column('vibe_id', sa.Integer(), nullable=False),
    sa.Column('vibe', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('vibe_id')
    )
    op.create_table('weather',
    sa.Column('weather_id', sa.Integer(), nullable=False),
    sa.Column('weather', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('weather_id')
    )
    op.create_table('albums',
    sa.Column('album_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.Text(), nullable=False),
    sa.Column('release_date', sa.Date(), nullable=False),
    sa.Column('genre_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['genre_id'], ['genres.genre_id'], ),
    sa.PrimaryKeyConstraint('album_id')
    )
    op.create_table('album_artist',
    sa.Column('album_artist_id', sa.Integer(), nullable=False),
    sa.Column('album_id', sa.Integer(), nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['album_id'], ['albums.album_id'], ),
    sa.ForeignKeyConstraint(['artist_id'], ['artists.artist_id'], ),
    sa.PrimaryKeyConstraint('album_artist_id')
    )
    op.create_table('tracks',
    sa.Column('track_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.Text(), nullable=False),
    sa.Column('runtime', sa.Integer(), nullable=False),
    sa.Column('genre_id', sa.Integer(), nullable=False),
    sa.Column('album_id', sa.Integer(), nullable=False),
    sa.Column('weather_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['album_id'], ['albums.album_id'], ),
    sa.ForeignKeyConstraint(['genre_id'], ['genres.genre_id'], ),
    sa.ForeignKeyConstraint(['weather_id'], ['weather.weather_id'], ),
    sa.PrimaryKeyConstraint('track_id')
    )
    op.create_table('playlist_track',
    sa.Column('playlist_track_id', sa.Integer(), nullable=False),
    sa.Column('playlist_id', sa.Integer(), nullable=False),
    sa.Column('track_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['playlist_id'], ['playlists.playlist_id'], ),
    sa.ForeignKeyConstraint(['track_id'], ['tracks.track_id'], ),
    sa.PrimaryKeyConstraint('playlist_track_id')
    )
    op.create_table('track_artist',
    sa.Column('track_artist_id', sa.Integer(), nullable=False),
    sa.Column('track_id', sa.Integer(), nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['artists.artist_id'], ),
    sa.ForeignKeyConstraint(['track_id'], ['tracks.track_id'], ),
    sa.PrimaryKeyConstraint('track_artist_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('track_artist')
    op.drop_table('playlist_track')
    op.drop_table('tracks')
    op.drop_table('album_artist')
    op.drop_table('albums')
    op.drop_table('weather')
    op.drop_table('vibe')
    op.drop_table('playlists')
    op.drop_table('genres')
    op.drop_table('artists')
    # ### end Alembic commands ###
