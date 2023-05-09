from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db
from fastapi.params import Query
from pydantic import BaseModel
from datetime import date
import sqlalchemy as sa

router = APIRouter()


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
    - birthday: date
    - gender: string
    - deathday: date or null

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
