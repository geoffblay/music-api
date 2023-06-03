from fastapi import APIRouter, HTTPException, Query
from enum import Enum
from src import database as db, weather
from pydantic import BaseModel
import sqlalchemy as sa

router = APIRouter()


class PlaylistJson(BaseModel):
    name: str
    track_ids: list[int]
    user_id: int


@router.delete("/playlists/{playlist_id}", tags=["playlists"])
def delete_playlist(playlist_id: int):
    """
    This endpoint deletes a playlist by its identifier.
    """
    if not db.try_parse(int, playlist_id):
        raise HTTPException(status_code=422, detail="Playlist ID must be an integer")

    check_playlist_stmt = sa.text(
        """
        SELECT COUNT(*)
        FROM playlists
        WHERE playlist_id = :playlist_id
        """
    )

    with db.engine.begin() as conn:
        result = conn.execute(
            check_playlist_stmt, {"playlist_id": playlist_id}
        ).scalar()
        if result == 0:
            raise HTTPException(
                status_code=422, detail=f"Playlist {playlist_id} not found"
            )

        conn.execute(
            sa.delete(db.playlists).where(db.playlists.c.playlist_id == playlist_id)
        )
    return {"message": "Playlist deleted."}


@router.delete("/playlists/{playlist_id}/tracks/{track_id}", tags=["playlists"])
def delete_track_from_playlist(playlist_id: int, track_id: int):
    """
    This endpoint deletes a track from a playlist by its identifier.
    """
    if not db.try_parse(int, playlist_id):
        raise HTTPException(status_code=422, detail="Playlist ID must be an integer")

    if not db.try_parse(int, track_id):
        raise HTTPException(status_code=422, detail="Track ID must be an integer")

    with db.engine.begin() as conn:
        playlist = conn.execute(
            sa.select(db.playlists).where(db.playlists.c.playlist_id == playlist_id)
        ).first()
        if not playlist:
            raise HTTPException(
                status_code=422, detail=f"Playlist {playlist_id} not found"
            )

        track = conn.execute(
            sa.select(db.tracks).where(db.tracks.c.track_id == track_id)
        ).first()
        if not track:
            raise HTTPException(status_code=422, detail=f"Track {track_id} not found")

        conn.execute(
            sa.delete(db.playlist_track).where(
                sa.and_(
                    db.playlist_track.c.playlist_id == playlist_id,
                    db.playlist_track.c.track_id == track_id,
                )
            )
        )
    return {"message": f"Track {track_id} deleted from playlist {playlist_id}."}


def get_score(weather, time, temperature, mood):
    score = 0

    # TEMPERATURE
    score += temperature * 4

    # TIME OF DAY
    if (
        int(time.split(":")[0]) >= 18
        or int(time.split(":")[0]) <= 6
    ):
        score += 0
    else:
        score += 400

    # WEATHER
    with db.engine.begin() as conn:
        sql = """
        SELECT weather_rating 
        FROM weather 
        WHERE weather = :cond
        """

        print(weather)
        result = conn.execute(
            sa.text(sql), [{"cond": weather}]
        ).fetchone()
        score += result[0]
    
    # MOOD
    if mood == "happy":
       score += 343
    elif mood == "party":
        score += 286
    elif mood == "workout":
        score += 229
    elif mood == "focus":
        score += 171
    elif mood == "chill":
        score += 114
    elif mood == "sleep":
        score += 57
    elif mood == "heartbroken":
        score += 0
    else:
        raise HTTPException(
            status_code=422,
            detail="Invalid vibe.",
        )
    
    print(score)
    return score / 4


@router.get("/playlists/generate", tags=["playlists"])
def generate(
    location: str = "San Luis Obispo",
    mood: str = "happy",
    num_tracks: int = Query(10, ge=1, le=100),
):
    """
    This endpoint will return an auto-generated playlist based on the user's location, time, and vibe.
    * `tracks`: a list of tracks associated with the playlist.

    Each track is represented by a dictionary with the following keys:
    * `track_id`: the internal id of the track.
    * `title`: the title of the track.
    * `runtime`: the runtime of the track.
    * `genre`: the genre of the track.
    * `artists`: a list of artists associated with the track.

    Each artist is represented by a dictionary with the following keys:
    * `artist_id`: the internal id of the artist.
    * `name`: the name of the artist.

    You can curate the playlist to your liking by specifying the following parameters:
    * `location`: specifying location will return tracks that match the current weather and time in a given location.
    Location must be a valid city, US zip, or lat,long (decimal degree, e.g: 35.2828,120.6596).
    * `mood`: specifying mood will return tracks that match the vibe of the playlist. Mood must be one of the following:
        - happy
        - party
        - workout
        - focus
        - chill
        - sleep
        - heartbroken
    * `num_tracks`: specifying num_tracks will return a playlist with the specified number of tracks.

    """
    
    if not db.try_parse(str, location):
        raise HTTPException(
            status_code=422,
            detail="Location must be a string.",
        )
    
    if not db.try_parse(str, mood):
        raise HTTPException(
            status_code=422,
            detail="Vibe must be a string.",
        )
    
    weather_data = weather.get_weather_data(location)
    if "error" in weather_data:
        raise HTTPException(
            status_code=422,
            detail=weather_data["error"],
        )
    
    score = get_score(weather_data["weather"], weather_data["time"], weather_data["temperature"], mood)

    with db.engine.begin() as conn:
        sql = """
        SELECT t.track_id, t.title, t.runtime, t.genre, a.artist_id, a.name
        FROM tracks AS t
        JOIN track_artist AS ta ON t.track_id = ta.track_id
        JOIN artists AS a ON ta.artist_id = a.artist_id
        ORDER BY ABS(:score - t.vibe_score)
        LIMIT :num_tracks
        """
        result = conn.execute(
            sa.text(sql), [{"score": score, "num_tracks": num_tracks}]
        ).fetchall()

        tracks = {}
        for row in result:
            if row[0] not in tracks:
                tracks[row[0]] = {
                    "title": row[1],
                    "runtime": row[2],
                    "genre": row[3],
                    "artists": [{"artist_id": row[4], "name": row[5]}],
                }
            else:
                tracks[row[0]]["artists"].append({"artist_id": row[4], "name": row[5]})

        return {"tracks": list(tracks.values())}


    


@router.put("/playlists/{playlist_id}/track/{track_id}", tags=["playlists"])
def add_track_to_playlist(playlist_id: int, track_id: int):
    """
    This endpoint adds a track to a playlist

    The endpoint accepts a JSON object with the following fields:
    * `playlist_id`: the id of the playlist
    * `track_id`: the id of the track

    The endpoint returns the id of the resulting playlist that was created.
    """

    if not db.try_parse(int, playlist_id):
        raise HTTPException(status_code=422, detail="Playlist ID must be an integer")

    if not db.try_parse(int, track_id):
        raise HTTPException(status_code=422, detail="Track ID must be an integer")

    with db.engine.begin() as conn:
        playlist = conn.execute(
            sa.select(db.playlists).where(db.playlists.c.playlist_id == playlist_id)
        ).first()
        if not playlist:
            raise HTTPException(
                status_code=422, detail=f"Playlist {playlist_id} not found"
            )

        track = conn.execute(
            sa.select(db.tracks).where(db.tracks.c.track_id == track_id)
        ).first()
        if not track:
            raise HTTPException(status_code=422, detail=f"Track {track_id} not found")

        new_playlist_track_stmt = sa.insert(db.playlist_track).values(
            {
                "playlist_id": playlist_id,
                "track_id": track_id,
            }
        )
        conn.execute(new_playlist_track_stmt)

    return {"message": f"Track {track_id} added to playlist {playlist_id}."}


@router.post("/playlists/", tags=["playlists"])
def add_playlist(playlist: PlaylistJson):
    """
    This endpoint adds a playlist to the database

    The endpoint accepts a JSON object with the following fields:
    * `name`: the name of the playlist
    * `track_ids`: a list of track ids
    * `user_id`: the id of the user

    The endpoint returns the id of the resulting playlist that was created.
    """

    # Null check for playlist name
    if not playlist.name:
        raise HTTPException(status_code=400, detail="Playlist name cannot be null.")

    # Check if all tracks exist
    check_tracks_stmt = sa.text(
        """
        SELECT COUNT(*)
        FROM tracks
        WHERE track_id = ANY(:track_ids)
    """
    )

    check_users_stmt = sa.text(
        """
        SELECT COUNT(*)
        FROM users
        WHERE user_id = :user_id
        """
    )

    with db.engine.begin() as conn:
        count = conn.execute(
            check_tracks_stmt, {"track_ids": playlist.track_ids}
        ).scalar()
        if count != len(playlist.track_ids):
            raise HTTPException(
                status_code=400, detail="One or more track ids does not exist."
            )

        count = conn.execute(check_users_stmt, {"user_id": playlist.user_id}).scalar()
        if count == 0:
            raise HTTPException(status_code=400, detail="User does not exist.")

        new_playlist_stmt = sa.insert(db.playlists).values(
            {"name": playlist.name, "user_id": playlist.user_id}
        )
        result = conn.execute(new_playlist_stmt)

        values = [
            {"playlist_id": result.inserted_primary_key[0], "track_id": track_id}
            for track_id in playlist.track_ids
        ]
        new_playlist_track_stmt = sa.insert(db.playlist_track)
        conn.execute(new_playlist_track_stmt, values)

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
            raise HTTPException(status_code=422, detail="Playlist not found")
