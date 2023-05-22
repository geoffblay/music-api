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
        
    raise HTTPException(status_code=404, detail="album not found.")
