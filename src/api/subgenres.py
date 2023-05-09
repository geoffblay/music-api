from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db
from fastapi.params import Query
from pydantic import BaseModel
from datetime import date
import sqlalchemy as sa

router = APIRouter()


class GenreJson(BaseModel):
    name: str


@router.post("/genres/", tags=["genres"])
def add_genre(genre: GenreJson):
    if genre.name == None:
        raise HTTPException(status_code=404, detail="Genre cannot be null.")

    new_genre_stmt = sa.insert(db.subgenres).values(
        {
            "name": genre.name.lower(),
        }
    )

    with db.engine.connect() as conn:
        result = conn.execute(new_genre_stmt)
        conn.commit()

        return result.inserted_primary_key[0]
