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


@router.get("/genres/", tags=["genres"])
def get_genre(genre_id: int):
    get_genre_stmt = (
        sa.select(db.subgenres.c.name)
        .select_from(db.subgenres)
        .where(db.subgenres.c.genre_id == genre_id)
    )

    with db.engine.connect() as conn:
        result = conn.execute(get_genre_stmt)
        if result:
            json = {"genre_id": genre_id, "name": result.name}
            return json
