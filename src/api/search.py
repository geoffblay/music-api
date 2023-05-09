from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db
from fastapi.params import Query
import sqlalchemy

router = APIRouter()

# class search_sort_options(str, Enum):
#     title = "title"
#     artist = "artist"
#     album = "album"
#     genre = "genre"
#     release_date = "release_date"


@router.get("/search/", tags=["search"])
def search(
    name: str = "",
    limit: int = Query(50, ge=1, le=250),
    offset: int = Query(0, ge=0),
    # sort: search_sort_options = search_sort_options.title,
):
    """
    This endpoint returns all of the search results for the given query.

    * `track_id`: the internal id of the track.
    * `title`: the title of the track.
    * `artists`: the artist of the track.
    * `album`: the album the track is from.
    * `runtime`: length of the track.
    * `genre`: genre of the track.

    Each artist is represented by a dictionary with the following keys:
    * `artist_id`: the internal id of the artist.
    * `name`: The name of the artist.
    """


    with db.engine.connect() as conn:
        # get all tracks where the titile is like title
        tracks = conn.execute(
            sqlalchemy.select(db.tracks)
            .where(db.tracks.c.title.ilike(f"%{name}%"))
            .limit(limit)
            .offset(offset)
        ).fetchall()
        tracks = [t._asdict() for t in tracks]

        # get all artists where the name is like name
        artists = conn.execute(
            sqlalchemy.select(db.artists)
            .where(db.artists.c.name.ilike(f"%{name}%"))
            .limit(limit)
            .offset(offset)
        ).fetchall()
        artists = [a._asdict() for a in artists]

        # get all albums where the title is like title
        albums = conn.execute(
            sqlalchemy.select(db.albums)
            .where(db.albums.c.title.ilike(f"%{name}%"))
            .limit(limit)
            .offset(offset)
        ).fetchall()
        albums = [a._asdict() for a in albums]

    if not artists and not tracks and not albums:
        raise HTTPException(status_code=404, detail="No results.")        

    json = {
        "tracks": tracks,
        "artists": artists,
        "albums": albums,
    }

    return json
