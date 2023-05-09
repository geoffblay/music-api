from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db
from fastapi.params import Query
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


@router.post("/albums/", tags=["albums"])
def add_album(album: AlbumJson):
    """
    This endpoint adds an album to the database

    The endpoint accepts a JSON object with the following fields:
    - title: string
    - release_date: date
    - artists: list[ArtistJson]
    - tracks: list[TrackJson]
    - genre_id: int

    Where TrackJson is:
    - track_id: int
    - title: string
    - artists: list[ArtistJson]
    - runtime: int

    Where ArtistJson is:
    - artist_id: int

    The endpoint returns the id of the resulting album that was created.
    """

    with db.engine.connect() as conn:
        new_album_stmt = sa.insert(db.albums).values(
            {
                "title": album.title,
                "release_date": album.release_date,
                "genre_id": album.genre_id,
            }
        )
        result = conn.execute(new_album_stmt)

        for track in album.tracks:
            new_track_stmt = sa.insert(db.tracks).values(
                {
                    "name": track.title,
                    "runtime": track.runtime,
                    "genre_id": album.genre_id,
                    "album_id": result.inserted_primary_key[0],
                    "release_date": album.release_date,
                }
            )
            t_result = conn.execute(new_track_stmt)

            for artist in track.artists:
                new_track_artist_stmt = sa.insert(db.track_artist).values(
                    {
                        "track_id": t_result.inserted_primary_key[0],
                        "artist_id": artist.artist_id,
                    }
                )
                conn.execute(new_track_artist_stmt)

        for artist in album.artists:
            new_album_artist_stmt = sa.insert(db.album_artist).values(
                    {
                        "album_id": result.inserted_primary_key[0],
                        "artist_id": artist.artist_id,
                    }
                )
            conn.execute(new_album_artist_stmt)

        conn.commit()

        return result.inserted_primary_key[0]
