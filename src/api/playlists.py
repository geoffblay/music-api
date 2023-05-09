from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db
from fastapi.params import Query
from pydantic import BaseModel
import sqlalchemy as sa
from datetime import date

router = APIRouter()


class PlaylistJson(BaseModel):
    name: str
    tracks: list[int]


@router.post("/playlists/", tags=["playlists"])
def add_playlist(playlist: PlaylistJson):
    """
    This endpoint adds an album to the database

    The endpoint accepts a JSON object with the following fields:
    - title: string
    - tracks: a list of track_ids for the playlist

    The endpoint returns the id of the resulting playlist that was created.
    """

    with db.engine.connect() as conn:
        new_playlist_stmt = sa.insert(db.playlists).values({"name": playlist.name})
        result = conn.execute(new_playlist_stmt)

        for track in playlist.tracks:
            new_playlist_track_stmt = sa.insert(db.playlist_track).values(
                {
                    "playlist_id": result.inserted_primary_key[0],
                    "track_id": track,
                }
            )
            conn.execute(new_playlist_track_stmt)

        conn.commit()

        return result.inserted_primary_key[0]


@router.get("/playlists/{playlist_id}", tags=["playlists"])
def get_playlist(playlist_id: int):
    """
    This endpoint returns a single playlist by its identifier. For each playlist, the following information is returned:
    * `playlist_id`: the internal id of the playlist.
    * `name`: the name of the playlist.
    * `tracks`: a list of tracks associated with the playlist.

    Each track is represented by a dictionary with the following keys:
    * `track_id`: the internal id of the track.
    * `title`: the title of the track.
    * `runtime`: the runtime of the track.
    * `artists`: a list of artists associated with the track.

    Each artist is represented by a dictionary with the following keys:
    * `artist_id`: the internal id of the artist.
    * `name`: the name of the artist.
    """
    with db.engine.connect() as conn:
        playlist = conn.execute(
            sa.select(db.playlists).where(db.playlists.c.playlist_id == playlist_id)
        ).fetchone()

        if playlist:
            tracks = conn.execute(
                sa.select(db.tracks)
                .select_from(db.tracks.join(db.playlist_track))
                .where(db.playlist_track.c.playlist_id == playlist_id)
            ).fetchall()
            tracks = [t._asdict() for t in tracks]

            for track in tracks:
                artists = conn.execute(
                    sa.select(db.artists)
                    .select_from(db.artists.join(db.track_artist))
                    .where(db.track_artist.c.track_id == track["track_id"])
                ).fetchall()
                track["artists"] = [a._asdict() for a in artists]

            playlist = playlist._asdict()
            playlist["tracks"] = tracks
            return playlist
        else:
            raise HTTPException(status_code=404, detail="Playlist not found")
