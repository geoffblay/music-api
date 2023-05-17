import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Albums(Base):
    __tablename__ = "albums"
    album_id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String(160), nullable=False)
    release_date = sa.Column(sa.Date, nullable=False)
    subgenre_id = sa.Column(
        sa.Integer, sa.ForeignKey("subgenres.subgenre_id"), nullable=False
    )


class SubGenres(Base):
    __tablename__ = "subgenres"
    subgenre_id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(160), nullable=False)


class Artists(Base):
    __tablename__ = "artists"
    artist_id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(160), nullable=False)
    gender = sa.Column(sa.String(160), nullable=False)
    deathdate = sa.Column(sa.Date, nullable=True)
    birthdate = sa.Column(sa.Date, nullable=True)


class Tracks(Base):
    __tablename__ = "tracks"
    track_id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String(160), nullable=False)
    runtime = sa.Column(sa.Integer, nullable=False)
    subgenre_id = sa.Column(sa.ForeignKey("subgenres.subgenre_id"), nullable=False)
    album_id = sa.Column(sa.ForeignKey("albums.album_id"), nullable=False)


class Playlists(Base):
    __tablename__ = "playlists"
    playlist_id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(160), nullable=False)


class Playlist_Track(Base):
    __tablename__ = "playlist_track"
    playlist_track_id = sa.Column(sa.Integer, primary_key=True)
    playlist_id = sa.Column(sa.ForeignKey("playlists.playlist_id"), nullable=False)
    track_id = sa.Column(sa.ForeignKey("tracks.track_id"), nullable=False)


class Album_Artist(Base):
    __tablename__ = "album_artist"
    album_artist_id = sa.Column(sa.Integer, primary_key=True)
    album_id = sa.Column(sa.ForeignKey("albums.album_id"), nullable=False)
    artist_id = sa.Column(sa.ForeignKey("artists.artist_id"), nullable=False)


class Track_Artist(Base):
    __tablename__ = "track_artist"
    track_artist_id = sa.Column(sa.Integer, primary_key=True)
    track_id = sa.Column(sa.ForeignKey("tracks.track_id"), nullable=False)
    artist_id = sa.Column(sa.ForeignKey("artists.artist_id"), nullable=False)
