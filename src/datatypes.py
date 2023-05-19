import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Albums(Base):
    __tablename__ = "albums"
    album_id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.Text, nullable=False)
    release_date = sa.Column(sa.Date, nullable=False)
    genre_id = sa.Column(sa.Integer, sa.ForeignKey("genres.genre_id"), nullable=False)


class Genres(Base):
    __tablename__ = "genres"
    genre_id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.Text, nullable=False)


class Artists(Base):
    __tablename__ = "artists"
    artist_id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.Text, nullable=False)
    gender = sa.Column(sa.Text, nullable=True)
    deathdate = sa.Column(sa.Date, nullable=True)
    birthdate = sa.Column(sa.Date, nullable=True)


class Tracks(Base):
    __tablename__ = "tracks"
    track_id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.Text, nullable=False)
    runtime = sa.Column(sa.Integer, nullable=False)
    genre_id = sa.Column(sa.ForeignKey("genres.genre_id"), nullable=False)
    album_id = sa.Column(sa.ForeignKey("albums.album_id"), nullable=False)
    weather_id = sa.Column(sa.ForeignKey("weather.weather_id"), nullable=False)


class Weather(Base):
    __tablename__ = "weather"
    weather_id = sa.Column(sa.Integer, primary_key=True)
    weather = sa.Column(sa.Text, nullable=False)


class Vibe(Base):
    __tablename__ = "vibe"
    vibe_id = sa.Column(sa.Integer, primary_key=True)
    vibe = sa.Column(sa.Text, nullable=False)


class Playlists(Base):
    __tablename__ = "playlists"
    playlist_id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.Text, nullable=False)


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
