from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db
from fastapi.params import Query
from pydantic import BaseModel
from datetime import date
import sqlalchemy as sa
from datetime import date

router = APIRouter()


@router.get("/tracks/{track_id}", tags=["tracks"])
def get_track(track_id: int):
    """
    This endpoint returns a single track by its identifier. For each track, the following information is returned:
    * `track_id`: the internal id of the track.
    * `title`: the title of the track.
    * `runtime`: the runtime of the track.
    * `genre`: the genre id of the track.
    * `release_date`: the release date of the track.
    * `album`: the name of the album of the track.
    * `artists`: a list of artists associated with the track.

    Each artist is represented by a dictionary with the following keys:
    * `artist_id`: the internal id of the artist.
    * `name`: the name of the artist.

    """

    with db.engine.connect() as conn:
        track = conn.execute(
            sa.select(db.tracks).where(db.tracks.c.track_id == track_id)
        ).fetchone()

        if track:
            artists = conn.execute(
                sa.select(db.artists.c.artist_id, db.artists.c.name)
                .select_from(db.artists.join(db.track_artist))
                .where(db.track_artist.c.track_id == track_id)
            ).fetchall()
            artists = [a._asdict() for a in artists]

            genre = conn.execute(
                sa.select(db.subgenres.c.name)
                .select_from(db.subgenres)
                .where(db.subgenres.c.genre_id == track.genre_id)
            ).fetchone()
            genre = genre._asdict()

            album = conn.execute(
                sa.select(db.albums)
                .select_from(db.albums.join(db.tracks))
                .where(db.tracks.c.track_id == track_id)
            ).fetchone()
            album = album._asdict()

            track = track._asdict()
            del track["genre_id"]
            del track["album_id"]

            track["artists"] = artists
            track["genre"] = genre["name"]
            track["album"] = album["title"]

            return track

        else:
            raise HTTPException(status_code=404, detail="Track not found.")


# class TrackJson(BaseModel):
#     title: str
#     album_id: int = None
#     runtime: int
#     genre_id: int
#     release_date: date
#     artist_ids: list[int]


# @router.post("/tracks/", tags=["tracks"])
# def add_track(track: TrackJson):
#     """ """

#     # null checks
#     if track.title == None:
#         raise HTTPException(status_code=404, detail="Title cannot be null.")

#     if track.runtime and track.runtime < 1:
#         raise HTTPException(
#             status_code=422, detail="Runtime cannot be null or less than 1."
#         )

#     if track.release_date == None:
#         raise HTTPException(status_code=404, detail="Release year cannot be null.")

#     if track.genre_id == None:
#         raise HTTPException(status_code=404, detail="Genre cannot be null.")

#     check_album_exists_stmt = (
#         sa.select(db.albums.c.album_id)
#         .select_from(db.albums)
#         .where(db.albums.c.album_id == track.album_id)
#     )

#     check_artist_matches_album_stmt = (
#         sa.select(db.artists.c.artist_id)
#         .select_from(db.albums)
#         .where(db.albums.c.album_id == track.album_id)
#     )

#     check_genre_exists_stmt = (
#         sa.select(db.subgenres.c.genre_id)
#         .select_from(db.subgenres)
#         .where(db.subgenres.c.genre_id == track.genre_id)
#     )

#     with db.engine.connect() as conn:
#         if not (conn.execute(check_album_exists_stmt)):
#             raise HTTPException(status_code=404, detail="Album not found.")

#         if track.album_id:
#             artist_id = conn.execute(check_artist_matches_album_stmt).fetchone()
#             if artist_id != track.artist_id:
#                 raise HTTPException(status_code=404, detail="Artist not found.")

#         if not (conn.execute(check_genre_exists_stmt)):
#             raise HTTPException(status_code=404, detail="Genre not found.")

#         new_track_stmt = sa.insert(db.tracks).values(
#             {
#                 "title": track.title.lower(),
#                 "album_id": track.album_id,
#                 "runtime": track.runtime,
#                 "genre_id": track.genre_id,
#                 "release_date": track.release_date,
#             }
#         )
#         result = conn.execute(new_track_stmt)
#         conn.commit()

#         for artist_id in track.artist_ids:
#             new_track_artist_stmt = sa.insert(db.track_artist).values(
#                 {
#                     "track_id": result.inserted_primary_key[0],
#                     "artist_id": artist_id,
#                 }
#             )
#             conn.execute(new_track_artist_stmt)
#             conn.commit()

#         return result.inserted_primary_key[0]
