from fastapi import APIRouter, HTTPException
from src import database as db, weather
from pydantic import BaseModel
import sqlalchemy as sa

router = APIRouter()


@router.get("/search/", tags=["search"])
def search(type: str = "tracks", name: str = "", limit: int = 10):
    """
    This endpoint searches the entire database for either tracks, albums, or artists.
    The type of search is specified by the `type` parameter, which can be one of `tracks`, `albums`, or `artists`.
    For tracks, a list of tracks is returned where each track is a dictionary with the following keys:
    * `track_id`: the unique id of the track
    * `title`: the title of the track
    * `runtime`: the duration of the track in seconds
    * `album_title`: the title of the album
    * `artist_names`: a list of the names of the artists

    For albums, a list of albums is returned where each album is a dictionary with the following keys:
    * `album_id`: the unique id of the album
    * `title`: the title of the album
    * `artist_names`: a list of the names of the artists
    * `release_date`: the release date of the album

    For artists, a list of artists is returned where each artist is a dictionary with the following keys:
    * `artist_id`: the unique id of the artist
    * `name`: the name of the artist
    """

    if limit < 1:
        raise HTTPException(status_code=422, detail="Limit must be greater than 0.")

    if type == "tracks":
        with db.engine.begin() as conn:
            sql = """
            SELECT t1.track_id, t.title AS track_title, t.runtime, al.title AS album_title, ar.name, al.album_id
            FROM tracks AS t
            JOIN 
            (
            SELECT track_id
            FROM tracks
            WHERE title LIKE '%' || :name || '%'
            LIMIT :limit
            ) AS t1 ON t1.track_id = t.track_id
            JOIN albums AS al ON t.album_id = al.album_id
            JOIN track_artist AS ta ON ta.track_id = t1.track_id
            JOIN artists AS ar ON ar.artist_id = ta.artist_id
            """
            result = conn.execute(
                sa.text(sql), [{"name": name, "limit": limit}]
            ).fetchall()

            if result:
                json = {
                    "tracks": [
                        {
                            "track_id": track.track_id,
                            "title": track.track_title,
                            "runtime": track.runtime,
                            "album_title": track.album_title,
                            "album_id": track.album_id,
                            "artist_names_and_respective_id": {
                                (row.name, row.artist_id)
                                for row in result
                                if row.track_id == track.track_id
                            },
                        }
                        for track in result
                    ]
                }

                return json

            else:
                raise HTTPException(status_code=422, detail="No tracks found.")

    elif type == "albums":
        sql = """
        SELECT t1.album_id, al.title, ar.name, al.release_date
        FROM albums AS al
        JOIN
        (
        SELECT album_id
        FROM albums
        WHERE title LIKE '%' || :name || '%'
        LIMIT :limit
        ) AS t1 ON t1.album_id = al.album_id
        JOIN album_artist AS aa ON aa.album_id = al.album_id
        JOIN artists AS ar ON ar.artist_id = aa.artist_id
        """
        with db.engine.begin() as conn:
            result = conn.execute(
                sa.text(sql), [{"name": name, "limit": limit}]
            ).fetchall()

            if result:
                json = {
                    "albums": [
                        {
                            "album_id": album.album_id,
                            "title": album.title,
                            "artist_names": {
                                row.name
                                for row in result
                                if row.album_id == album.album_id
                            },
                            "release_date": album.release_date,
                        }
                        for album in result
                    ]
                }

                return json

            else:
                raise HTTPException(status_code=422, detail="No albums found.")

    elif type == "artists":
        sql = """
        SELECT artist_id, name
        FROM artists
        WHERE name LIKE '%' || :name || '%'
        LIMIT :limit
        """
        with db.engine.begin() as conn:
            result = conn.execute(
                sa.text(sql), [{"name": name, "limit": limit}]
            ).fetchall()

            if result:
                json = {
                    "artists": [
                        {"artist_id": row.artist_id, "name": row.name} for row in result
                    ]
                }

                return json

            else:
                raise HTTPException(status_code=422, detail="No artists found.")
    else:
        raise HTTPException(
            status_code=422,
            detail="Invalid type. Must be one of 'tracks', 'albums', or 'artists'.",
        )
