import csv
import os
import io
from supabase import Client, create_client
import dotenv
import sqlalchemy
from datetime import datetime


# Supabase and Engine setup
# *********************************************************************************


def database_connection_url():
    dotenv.load_dotenv()
    DB_USER: str = os.environ.get("POSTGRES_USER")
    DB_PASSWD = os.environ.get("POSTGRES_PASSWORD")
    DB_SERVER: str = os.environ.get("POSTGRES_SERVER")
    DB_PORT: str = os.environ.get("POSTGRES_PORT")
    DB_NAME: str = os.environ.get("POSTGRES_DB")
    return f"postgresql://{DB_USER}:{DB_PASSWD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"


# DO NOT CHANGE THIS TO BE HARDCODED. ONLY PULL FROM ENVIRONMENT VARIABLES.
dotenv.load_dotenv()
supabase_api_key = os.environ.get("SUPABASE_API_KEY")
supabase_url = os.environ.get("SUPABASE_URL")

# create the database engine
engine = sqlalchemy.create_engine(database_connection_url())


if supabase_api_key is None or supabase_url is None:
    raise Exception(
        "You must set the SUPABASE_API_KEY and SUPABASE_URL environment variables."
    )


supabase: Client = create_client(supabase_url, supabase_api_key)

sess = supabase.auth.get_session()

metadata_obj = sqlalchemy.MetaData()
# *********************************************************************************
# *********************************************************************************


def try_parse(type, val):
    try:
        return type(val)
    except ValueError:
        return None


tracks = sqlalchemy.Table("tracks", metadata_obj, autoload_with=engine)
playlists = sqlalchemy.Table("playlists", metadata_obj, autoload_with=engine)
albums = sqlalchemy.Table("albums", metadata_obj, autoload_with=engine)
subgenres = sqlalchemy.Table("subgenres", metadata_obj, autoload_with=engine)
artists = sqlalchemy.Table("artists", metadata_obj, autoload_with=engine)
