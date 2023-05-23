from fastapi import APIRouter, HTTPException
from src import database as db
from pydantic import BaseModel
from datetime import date
import sqlalchemy as sa
from datetime import date

router = APIRouter()


@router.get("/tracks/{track_id}", tags=["tracks"])
def get_track(track_id: int):
    """
    This endpoint returns a single track by its identifier. For each track, the following information is returned:
    * `track_id`: the internal id of the track.
    * `title`: the title of the track.
    * `runtime`: the runtime of the track.
    * `genre`: the genre of the track.
    * `release_date`: the release date of the track.
    * `album`: the name of the album of the track, if there is one.
    * `artists`: a list of artists associated with the track.

    Each artist is represented by a dictionary with the following keys:
    * `artist_id`: the internal id of the artist.
    * `name`: the name of the artist.
    """
    # get track information, if track exists
    track_stmt = sa.text(
        """
        SELECT t.track_id, t.title, t.runtime, t.genre, t.release_date, a.title AS album
        FROM tracks t
        LEFT JOIN albums AS a ON t.album_id = a.album_id
        WHERE t.track_id = :track_id
    """
    )

    # get artists associated with track
    artist_stmt = sa.text(
        """
        SELECT a.artist_id, a.name
        FROM artists AS a
        JOIN track_artist AS ta ON a.artist_id = ta.artist_id
        WHERE ta.track_id = :track_id
    """
    )

    with db.engine.begin() as conn:
        result = conn.execute(track_stmt, {"track_id": track_id}).fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Track not found.")

        # create dictionary to represent track
        track = result._asdict()

        # get artists associated with track
        result = conn.execute(artist_stmt, {"track_id": track_id}).fetchall()

        # create list of dictionaries to represent artists
        artists = [row._asdict() for row in result]
        track["artists"] = artists

        return track


class TrackJson(BaseModel):
    title: str
    album_id: int = None
    runtime: int
    genre: str = None
    release_date: date
    artist_ids: list[int]
    vibe_score: int


@router.post("/tracks/", tags=["tracks"])
def add_track(track: TrackJson):
    """
    This endpoint is used to add a new track to the database. The following information is required:
    * `title`: the title of the track.
    * `runtime`: the runtime of the track.
    * `genre`: the genre of the track, or null if unknown.
    * `release_date`: the release date of the track.
    * `artist_ids`: a list of artist ids associated with the track.
    * `vibe_score`: the vibe score of the track
    """
    # null and type checks
    if not db.try_parse(str, track.title) or track.title == None:
        raise HTTPException(status_code=422, detail="Title cannot be null.")

    if not db.try_parse(int, track.runtime) or track.runtime < 1:
        raise HTTPException(
            status_code=422, detail="Runtime cannot be null or less than 1."
        )

    if not track.genre or not db.try_parse(str, track.genre):
        raise HTTPException(status_code=422, detail="Genre must be a string.")

    if track.release_date == None:
        raise HTTPException(status_code=422, detail="Release year cannot be null.")

    if not db.try_parse(int, track.vibe_score) or (
        track.vibe_score < 1 or track.vibe_score > 400
    ):
        raise HTTPException(
            status_code=422, detail="Vibe score must be an integer between 1 and 400."
        )

    check_artist_stmt = sa.text(
        """
        SELECT COUNT(*)
        FROM artists AS a
        WHERE a.artist_id IN :artist_ids
    """
    )

    check_album_stmt = sa.text(
        """
        SELECT COUNT(*)
        FROM albums AS a
        WHERE a.album_id = :album_id
        """
    )

    with db.engine.begin() as conn:
        result = conn.execute(
            check_artist_stmt,
            {"artist_ids": tuple(track.artist_ids)},
        )
        count = result.scalar()

        # check if result matches number of artists, this checks album exists as well
        if count != len(track.artist_ids):
            raise HTTPException(
                status_code=404, detail="One or more artists not found."
            )

        result = conn.execute(check_album_stmt, {"album_id": track.album_id})
        if result.scalar() == 0 and track.album_id != None:
            raise HTTPException(status_code=404, detail="Album not found.")

        new_track_stmt = sa.text(
            """
            INSERT INTO tracks (title, album_id, runtime, genre, release_date, vibe_score)
            VALUES (:title, :album_id, :runtime, :genre, :release_date, :vibe_score)
            RETURNING track_id
        """
        )

        result = conn.execute(
            new_track_stmt,
            {
                "title": track.title.lower(),
                "album_id": track.album_id,
                "runtime": track.runtime,
                "genre": track.genre,
                "release_date": track.release_date,
                "vibe_score": track.vibe_score,
            },
        )
        track_id = result.scalar()

        # create entries to match artists to track
        # unnest function iterates through each artist id and adds a row for each
        new_track_artist_stmt = sa.text(
            """
            INSERT INTO track_artist (track_id, artist_id)
            SELECT :track_id, unnest(:artist_ids)
        """
        )

        conn.execute(
            new_track_artist_stmt,
            {"track_id": track_id, "artist_ids": track.artist_ids},
        )

        return track_id
