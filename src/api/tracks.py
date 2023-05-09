from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db
from fastapi.params import Query
from pydantic import BaseModel
import sqlalchemy as sa
from datetime import date


router = APIRouter()


class TrackJson(BaseModel):
    title: str
    album_id: str or None
    runtime: int
    genre_id: str
    release_date: date


@router.post("/tracks/", tags=["tracks"])
def add_track(track: TrackJson):
    """
    This endpoint adds an track to the database

    The endpoint accepts a JSON object with the following fields:
    - title: string
    - album_id: str or None
    - runtime: int
    - genre_id: str
    - release_date: date

    The endpoint returns the id of the resulting track that was created.
    """

    # null checks
    if track.title == None:
        raise HTTPException(status_code=404, detail="Title cannot be null.")

    if track.runtime == None:
        raise HTTPException(status_code=404, detail="Runtime cannot be null.")

    if track.release_year == None:
        raise HTTPException(status_code=404, detail="Release year cannot be null.")

    if track.genre_id == None:
        raise HTTPException(status_code=404, detail="Genre cannot be null.")

    check_album_exists_stmt = (
        sa.select(db.albums.c.album_id)
        .select_from(db.albums)
        .where(db.albums.c.album_id == track.album_id)
    )

    check_artist_matches_album_stmt = (
        sa.select(db.artists.c.artist_id)
        .select_from(db.albums)
        .where(db.albums.c.album_id == track.album_id)
    )

    with db.engine.connect() as conn:
        if not (conn.execute(check_album_exists_stmt)):
            raise HTTPException(status_code=404, detail="Album not found.")
        if track.album_id:
            artist_id = conn.execute(check_artist_matches_album_stmt).fetchone()
            if artist_id != track.artist_id:
                raise HTTPException(status_code=404, detail="Artist not found.")


@router.get("/tracks/{track_id}", tags=["tracks"])
def get_track(track_id: int):
    """
    This endpoint returns a single track by its identifier. For each track it returns:
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

    json = {"test"}
    return json

    # raise HTTPException(status_code=404, detail="track not found.")
