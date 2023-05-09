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

@router.get("/albums/{album_id}", tags=["albums"])
def get_album(album_id: int):
    """
    This endpoint returns a single album by its identifier. For each album, the following information is returned:
    * `album_id`: the internal id of the album.
    * `title`: the title of the album.
    * `release_date`: the release date of the album.
    * `genre`: the genre id of the album.
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

    with db.engine.connect() as conn:
        album = conn.execute(
            sa.select(db.albums).where(db.albums.c.album_id == album_id)
        ).fetchone()

        if album:
            artists = conn.execute(
                sa.select(db.artists)
                .select_from(db.artists.join(db.album_artist))
                .where(db.album_artist.c.album_id == album_id)
            ).fetchall()
            artists = [a._asdict() for a in artists]

            tracks = conn.execute(
                sa.select(db.tracks).where(db.tracks.c.album_id == album_id)
            ).fetchall()
            tracks = [t._asdict() for t in tracks]

            return {
                "album_id": album.album_id,
                "title": album.title,
                "release_date": album.release_date,
                "genre_id": album.genre_id,
                "artists": artists,
                "tracks": tracks,
            }
        
    raise HTTPException(status_code=404, detail="movie not found.")




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
                    "title": track.title,
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
