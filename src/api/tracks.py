from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db
from fastapi.params import Query
from pydantic import BaseModel
from datetime import date
import sqlalchemy as sa
from datetime import date

router = APIRouter()


class TrackJson(BaseModel):
    title: str
    album_id: int = None
    runtime: int
    genre_id: int
    release_date: date
    artist_ids: list[int]


@router.post("/tracks/", tags=["tracks"])
def add_track(track: TrackJson):
    """ """

    # null checks
    if track.title == None:
        raise HTTPException(status_code=404, detail="Title cannot be null.")

    if track.runtime and track.runtime < 1:
        raise HTTPException(
            status_code=404, detail="Runtime cannot be null or less than 1."
        )

    if track.release_date == None:
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

    check_genre_exists_stmt = (
        sa.select(db.subgenres.c.genre_id)
        .select_from(db.subgenres)
        .where(db.subgenres.c.genre_id == track.genre_id)
    )

    with db.engine.connect() as conn:
        if not (conn.execute(check_album_exists_stmt)):
            raise HTTPException(status_code=404, detail="Album not found.")

        if track.album_id:
            artist_id = conn.execute(check_artist_matches_album_stmt).fetchone()
            if artist_id != track.artist_id:
                raise HTTPException(status_code=404, detail="Artist not found.")

        if not (conn.execute(check_genre_exists_stmt)):
            raise HTTPException(status_code=404, detail="Genre not found.")

        new_track_stmt = sa.insert(db.tracks).values(
            {
                "title": track.title.lower(),
                "album_id": track.album_id,
                "runtime": track.runtime,
                "genre_id": track.genre_id,
                "release_date": track.release_date,
            }
        )
        result = conn.execute(new_track_stmt)
        conn.commit()

        for artist_id in track.artist_ids:
            new_track_artist_stmt = sa.insert(db.track_artist).values(
                {
                    "track_id": result.inserted_primary_key[0],
                    "artist_id": artist_id,
                }
            )
            conn.execute(new_track_artist_stmt)
            conn.commit()

        return result.inserted_primary_key[0]


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

    with db.engine.connect() as conn:
        track = conn.execute(
            sa.select(db.tracks).where(db.tracks.c.track_id == track_id)
        ).fetchone()

        if track:
            artists = conn.execute(
                sa.select(db.artists.c.artist_id, db.artists.c.name)
                .select_from(db.track_artist.join(db.artists))
                .where(db.track_artist.c.track_id == track_id)
            ).fetchall()

            album_title = conn.execute(
                sa.select(db.albums.c.title)
                .select_from(db.tracks.join(db.albums))
                .where(db.tracks.c.track_id == track_id)
            ).fetchone()

            genre = conn.execute(
                sa.select(db.subgenres.c.name)
                .select_from(db.tracks.join(db.subgenres))
                .where(db.tracks.c.track_id == track_id)
            ).fetchone()

            json = {
                "track_id": track.track_id,
                "title": track.title,
                "artists": artists,
                "album": album_title,
                "runtime": track.runtime,
                "genre": genre,
            }
    return json

    # raise HTTPException(status_code=404, detail="track not found.")
