from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db
from fastapi.params import Query
from pydantic import BaseModel
import sqlalchemy as sa
from datetime import date

router = APIRouter()


class AlbumJson(BaseModel):
    title: str
    release_date: date


@router.post("/albums/", tags=["albums"])
def add_album(album: AlbumJson):
    """
    This endpoint adds an album to the database

    The endpoint accepts a JSON object with the following fields:
    - title: string
    - release_date: date

    The endpoint returns the id of the resulting album that was created.
    """

    # null checks
    if album.title == None:
        raise HTTPException(status_code=404, detail="Title cannot be null.")

    if album.release_date == None:
        raise HTTPException(status_code=404, detail="Release date cannot be null.")

    with db.engine.connect() as conn:
        new_album_stmt = sa.insert(db.albums).values(
            {
                # "album_id": album_id,
                "title": album.title,
                "release_date": album.release_date,
            }
        )
        result = conn.execute(new_album_stmt)
        conn.commit()

        return result.inserted_primary_key[0]
