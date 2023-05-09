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
