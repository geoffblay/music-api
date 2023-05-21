from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db, weather
from pydantic import BaseModel
import sqlalchemy as sa

router = APIRouter()


class PlaylistJson(BaseModel):
    name: str
    track_ids: list[int]

@router.delete("/playlists/{playlist_id}", tags=["playlists"])
def delete_playlist(playlist_id: int):
    """
    This endpoint deletes a playlist by its identifier.
    """
    with db.engine.connect() as conn:
        conn.execute(
            sa.delete(db.playlists).where(db.playlists.c.playlist_id == playlist_id)
        )
    return {"message": "Playlist deleted."}

# TODO: Make a better system for adding and deleting tracks from playlist

@router.put("/playlists/{playlist_id}", tags=["playlists"])
def update_playlist(playlist_id: int, playlist: PlaylistJson):
    """
    This endpoint updates a playlist by its identifier.

    The endpoint accepts a JSON object with the following fields:
    - title: string
    - track_ids: a list of track_ids for the playlist
    """
    with db.engine.connect() as conn:
        conn.execute(
            sa.update(db.playlists)
            .where(db.playlists.c.playlist_id == playlist_id)
            .values({"name": playlist.name})
        )

        conn.execute(
            sa.delete(db.playlist_track).where(
                db.playlist_track.c.playlist_id == playlist_id
            )
        )

        for track in playlist.track_ids:
            conn.execute(
                sa.insert(db.playlist_track).values(
                    {"playlist_id": playlist_id, "track_id": track}
                )
            )

    return {"message": "Playlist updated."}

@router.get("/create/", tags=["playlists"])
def create(
    location: str="",
    time: str="",
    vibe: str="",
    num_tracks: int=0,
):
    """
    This endpoint will create and return an auto-generated playlist based on the user's location, time, and vibe.
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

    You can curate the playlist to your liking by specifying the following parameters:
    * `location`: specifying location will return tracks that match the current weather in a given location. 
    Location must be a valid city, US zip, or lat,long (decimal degree, e.g: 35.2828,120.6596).
    * `time`: specifying time will return tracks that match the time of day. Time must be in the format HH:MM.
    * `vibe`: specifying vibe will return tracks that match the vibe of the playlist. Vibe must be one of the following:
        - chill
        - party
        - workout
        - focus
        - sleep
    
    """
    if location:
        weather_data = weather.get_weather_data(location)
    
    print(weather_data)


@router.post("/playlists/", tags=["playlists"])
def add_playlist(playlist: PlaylistJson):
    """
    This endpoint adds an album to the database

    The endpoint accepts a JSON object with the following fields:
    - title: string
    - track_ids: a list of track_ids for the playlist

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
