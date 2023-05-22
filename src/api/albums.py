from fastapi import APIRouter, HTTPException
from src import database as db
from pydantic import BaseModel
import sqlalchemy as sa
from datetime import date

router = APIRouter()


class ArtistJson(BaseModel):
    artist_id: int


class TrackJson(BaseModel):
    title: str
    artists: list[ArtistJson]
    runtime: int


class AlbumJson(BaseModel):
    title: str
    release_date: date
    artists: list[ArtistJson]
    tracks: list[TrackJson]
    genre_id: int


@router.get("/albums/{album_id}", tags=["albums"])
def get_album(album_id: int):
    """
    This endpoint returns a single album by its identifier. For each album, the following information is returned:
    * `album_id`: the internal id of the album.
    * `title`: the title of the album.
    * `release_date`: the release date of the album.
    * `artists`: a list of artists associated with the album.
    * `tracks`: a list of tracks associated with the album.

    Each artist is represented by a dictionary with the following keys:
    * `artist_id`: the internal id of the artist.
    * `name`: the name of the artist.

    Each track is represented by a dictionary with the following keys:
    * `track_id`: the internal id of the track.
    * `title`: the title of the track.
    * `runtime`: the runtime of the track.

    """

    # get album, artist, and track information
    stmt = sa.text(
        """
        SELECT 
            a.album_id, a.title AS album_title, a.release_date, 
            ar.artist_id, ar.name,
            t.track_id, t.title AS track_title, t.runtime
        FROM 
            albums AS a
            JOIN album_artist AS aa ON a.album_id = aa.album_id
            JOIN artists AS ar ON aa.artist_id = ar.artist_id
            JOIN tracks AS t ON a.album_id = t.album_id
        WHERE 
            a.album_id = :album_id
        """
    )

    with db.engine.begin() as conn:
        result = conn.execute(stmt, {"album_id": album_id}).fetchall()
        if not result:
            raise HTTPException(status_code=404, detail="Album not found.")

        # convert result to list of dictionaries
        result = [row._asdict() for row in result]

        # Create dictionary to represent album for json return
        album = {
            "album_id": result[0]["album_id"],
            "title": result[0]["album_title"],
            "release_date": result[0]["release_date"],
            "artists": [],
            "tracks": [],
        }

        # add artists and tracks to album
        for row in result:
            if {"artist_id": row["artist_id"], "name": row["name"]} not in album[
                "artists"
            ]:
                # add artist to album if not already added
                album["artists"].append(
                    {"artist_id": row["artist_id"], "name": row["name"]}
                )

            if {
                "track_id": row["track_id"],
                "title": row["track_title"],
                "runtime": row["runtime"],
            } not in album["tracks"]:
                # add track to album if not already added
                album["tracks"].append(
                    {
                        "track_id": row["track_id"],
                        "title": row["track_title"],
                        "runtime": row["runtime"],
                    }
                )

        return album
