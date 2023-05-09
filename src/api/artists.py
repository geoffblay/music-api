from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db
from fastapi.params import Query
from pydantic import BaseModel
from datetime import date
import sqlalchemy as sa

router = APIRouter()


@router.get("/artists/{artist_id}", tags=["artists"])
def get_artist(artist_id: int):
    """
    This endpoint returns a single artist by its identifier. For each artist, the following information is returned:
    * `artist_id`: the internal id of the artist.
    * `name`: the name of the artist.
    * `birthdate`: the birthdate of the artist.
    * `deathdate`: the deathdate of the artist (if applicable).
    * `gender`: the gender of the artist.
    * `tracks`: a list of tracks associated with the artist.
    * `albums`: a list of albums associated with the artist.

    Each track is represented by a dictionary with the following keys:
    * `track_id`: the internal id of the track.
    * `title`: the title of the track.
    * `release_date`: the release date of the track.

    Each album is represented by a dictionary with the following keys:
    * `album_id`: the internal id of the album.
    * `title`: the title of the album.
    * `release_date`: the release date of the album.
    """

    with db.engine.connect() as conn:
        artist = conn.execute(
            sa.select(db.artists).where(db.artists.c.artist_id == artist_id)
        ).fetchone()

        if artist:
            tracks = conn.execute(
                sa.select(db.tracks.c.track_id, db.tracks.c.title, db.tracks.c.release_date)
                .select_from(db.tracks.join(db.track_artist))
                .where(db.track_artist.c.artist_id == artist_id)
            ).fetchall()
            tracks = [t._asdict() for t in tracks]

            albums = conn.execute(
                sa.select(db.albums.c.album_id, db.albums.c.title, db.albums.c.release_date)
                .select_from(db.albums.join(db.album_artist))
                .where(db.album_artist.c.artist_id == artist_id)
            ).fetchall()
            albums = [a._asdict() for a in albums]

            artist = artist._asdict()
            artist["tracks"] = tracks
            artist["albums"] = albums
            return artist

        else:
            raise HTTPException(status_code=404, detail="Artist not found.")


class ArtistJson(BaseModel):
    name: str
    birthdate: date
    gender: str
    deathdate: date = None


@router.post("/artists/", tags=["artists"])
def add_artist(artist: ArtistJson):
    """
    This endpoint adds an artist to the database

    The endpoint accepts a JSON object with the following fields:
    - name: string
    - birthdate: date
    - gender: string ("M" or "F")
    - deathdate: date or null

    The endpoint returns the id of the resulting artist that was created.
    """

    # null checks
    if artist.name == None:
        raise HTTPException(status_code=404, detail="Name cannot be null.")

    if artist.birthdate == None:
        raise HTTPException(status_code=404, detail="Birthday cannot be null.")

    if artist.gender == None:
        raise HTTPException(status_code=404, detail="Gender cannot be null.")

    # should we do some sort of check to see if the artist already exists?
    with db.engine.connect() as conn:
        new_artist_stmt = sa.insert(db.artists).values(
            {
                "name": artist.name.lower(),
                "birthdate": artist.birthdate,
                "deathdate": artist.deathdate,
                "gender": artist.gender,
            }
        )
        result = conn.execute(new_artist_stmt)
        conn.commit()

        return result.inserted_primary_key[0]
