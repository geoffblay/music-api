import os
import io
import dotenv
import sqlalchemy
from datetime import datetime


def database_connection_url():
    dotenv.load_dotenv()
    DB_USER: str = os.environ.get("POSTGRES_USER")
    DB_PASSWD = os.environ.get("POSTGRES_PASSWORD")
    DB_SERVER: str = os.environ.get("POSTGRES_SERVER")
    DB_PORT: str = os.environ.get("POSTGRES_PORT")
    DB_NAME: str = os.environ.get("POSTGRES_DB")
    return f"postgresql://{DB_USER}:{DB_PASSWD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"


def try_parse(type, val):
    try:
        return type(val)
    except ValueError:
        return None


# *********************************************************************************
# create the database engine

database_url = database_connection_url()
engine = sqlalchemy.create_engine(database_url)
metadata_obj = sqlalchemy.MetaData()

# *********************************************************************************

tracks = sqlalchemy.Table("tracks", metadata_obj, autoload_with=engine)
playlists = sqlalchemy.Table("playlists", metadata_obj, autoload_with=engine)
albums = sqlalchemy.Table("albums", metadata_obj, autoload_with=engine)
artists = sqlalchemy.Table("artists", metadata_obj, autoload_with=engine)
track_artist = sqlalchemy.Table("track_artist", metadata_obj, autoload_with=engine)
playlist_track = sqlalchemy.Table("playlist_track", metadata_obj, autoload_with=engine)
album_artist = sqlalchemy.Table("album_artist", metadata_obj, autoload_with=engine)
weather = sqlalchemy.Table("weather", metadata_obj, autoload_with=engine)
vibe = sqlalchemy.Table("vibe", metadata_obj, autoload_with=engine)
users = sqlalchemy.Table("users", metadata_obj, autoload_with=engine)

def try_parse(type, val):
    try:
        return type(val)
    except ValueError:
        return None
