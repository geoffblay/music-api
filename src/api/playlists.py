from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db, weather
from pydantic import BaseModel
import sqlalchemy as sa
import statistics

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
    vibe: str="",
    num_tracks: int=10,
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
    vals = {}

    if location:
        weather_data = weather.get_weather_data(location)

        vals["temp"] = weather_data["temperature"] * 4

        if int(weather_data["time"].split(':')[0]) >= 18 or int(weather_data["time"].split(':')[0]) <= 6:
            time_val = 0
        else:
            time_val = 400
        vals["time"] = time_val

        with db.engine.begin() as conn:
            sql = """
            SELECT weather_rating 
            FROM weather 
            WHERE weather = :cond
            """
            result = conn.execute(
                sa.text(sql), 
                [{"cond": weather_data["weather"]}]
            ).fetchone()
            vals["weather"] = result[0]
        

    if vibe:
        if vibe == "happy":
            vals['mood'] = 343
        elif vibe == "party":
            vals['mood'] = 286
        elif vibe == "workout":
            vals['mood'] = 229
        elif vibe == "focus":
            vals['mood'] = 171
        elif vibe == "chill":
            vals['mood'] = 114
        elif vibe == "sleep":
            vals['mood'] = 57
        elif vibe == "heartbroken":
            vals['mood'] = 0


    avg = sum(vals.values()) / len(vals)
    print(avg)
    

    with db.engine.begin() as conn:
        sql = """
        SELECT t.track_id, t.title, t.runtime, t.genre, a.artist_id, a.name
        FROM tracks AS t
        JOIN track_artist AS ta ON t.track_id = ta.track_id
        JOIN artists AS a ON ta.artist_id = a.artist_id
        ORDER BY ABS(:avg - t.vibe)
        LIMIT :num_tracks
        """
        result = conn.execute(
            sa.text(sql),
            [{"avg": avg, "num_tracks": num_tracks}]
        ).fetchall()
        
        tracks = {}
        for row in result:
            if row[0] not in tracks:
                tracks[row[0]] = {
                    "title": row[1],
                    "runtime": row[2],
                    "genre": row[3],
                    "artists": [{"artist_id": row[4], "name": row[5]}]
                }
            else:
                tracks[row[0]]["artists"].append({"artist_id": row[4], "name": row[5]})

        return {
            "tracks": list(tracks.values())
        }
        

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
