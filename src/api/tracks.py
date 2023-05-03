from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db
from fastapi.params import Query
import sqlalchemy

router = APIRouter()

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

    json = {'test'}
    return json

    # raise HTTPException(status_code=404, detail="track not found.")