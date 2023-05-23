from fastapi import APIRouter, HTTPException
from src import database as db
from pydantic import BaseModel
import sqlalchemy as sa
from datetime import date

router = APIRouter()


@router.get("/albums/{album_id}", tags=["albums"])
def get_album(album_id: int):
    """
    This endpoint returns a single album by its identifier. For each album, the following information is returned:
    * `album_id`: the internal id of the album.
    * `title`: the title of the album.
    * `release_date`: the release date of the album.
    * `artists`: a list of artists associated with the album.
    * `tracks`: a list of tracks associated with the album.

    Each artist is represented by a dictionary with the following keys:
    * `artist_id`: the internal id of the artist.
    * `name`: the name of the artist.

    Each track is represented by a dictionary with the following keys:
    * `track_id`: the internal id of the track.
    * `title`: the title of the track.
    * `runtime`: the runtime of the track.

    """

    if not db.try_parse(int, album_id):
        raise HTTPException(status_code=422, detail="Album ID must be an integer.")

    # get album, artist, and track information
    stmt = sa.text(
        """
        SELECT 
            a.album_id, a.title AS album_title, a.release_date, 
            ar.artist_id, ar.name,
            t.track_id, t.title AS track_title, t.runtime
        FROM 
            albums AS a
            JOIN album_artist AS aa ON a.album_id = aa.album_id
            JOIN artists AS ar ON aa.artist_id = ar.artist_id
            JOIN tracks AS t ON a.album_id = t.album_id
        WHERE 
            a.album_id = :album_id
        """
    )

    with db.engine.begin() as conn:
        result = conn.execute(stmt, {"album_id": album_id}).fetchall()
        if not result:
            raise HTTPException(status_code=404, detail="Album not found.")

        # convert result to list of dictionaries
        result = [row._asdict() for row in result]

        # Create dictionary to represent album for json return
        album = {
            "album_id": result[0]["album_id"],
            "title": result[0]["album_title"],
            "release_date": result[0]["release_date"],
            "artists": [],
            "tracks": [],
        }

        # add artists and tracks to album
        for row in result:
            if {"artist_id": row["artist_id"], "name": row["name"]} not in album[
                "artists"
            ]:
                # add artist to album if not already added
                album["artists"].append(
                    {"artist_id": row["artist_id"], "name": row["name"]}
                )

            if {
                "track_id": row["track_id"],
                "title": row["track_title"],
                "runtime": row["runtime"],
            } not in album["tracks"]:
                # add track to album if not already added
                album["tracks"].append(
                    {
                        "track_id": row["track_id"],
                        "title": row["track_title"],
                        "runtime": row["runtime"],
                    }
                )

        return album


@router.get("/recommend/", tags=["albums"])
def recommend(
    location: str = "",
    vibe: str = "",
    num_tracks: int = 10,
):
    """
    This endpoint will return an album based on a  location, the time of day at that location, the user's current
    mood, and the preferred number of tracks.
    * `album_id`: the internal id of the album.
    * `title`: the title of the album.
    * `release_date`: the release date of the album.
    * `genre`: the genre id of the album.
    * `artists`: a list of artists associated with the album.
    * `tracks`: a list of tracks associated with the album.

    Each artist is represented by a dictionary with the following keys:
    * `artist_id`: the internal id of the artist.
    * `name`: the name of the artist.

    Each track is represented by a dictionary with the following keys:
    * `track_id`: the internal id of the track.
    * `title`: the title of the track.
    * `runtime`: the runtime of the track.
    """
    vals = {}

    if location:
        weather_data = db.weather.get_weather_data(location)

        vals["temp"] = weather_data["temperature"] * 4

        if (
            int(weather_data["time"].split(":")[0]) >= 18
            or int(weather_data["time"].split(":")[0]) <= 6
        ):
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
                sa.text(sql), [{"cond": weather_data["weather"]}]
            ).fetchone()
            vals["weather"] = result[0]

    if vibe:
        if vibe == "happy":
            vals["mood"] = 343
        elif vibe == "party":
            vals["mood"] = 286
        elif vibe == "workout":
            vals["mood"] = 229
        elif vibe == "focus":
            vals["mood"] = 171
        elif vibe == "chill":
            vals["mood"] = 114
        elif vibe == "sleep":
            vals["mood"] = 57
        elif vibe == "heartbroken":
            vals["mood"] = 0

    avg = sum(vals.values()) / len(vals)

    with db.engine.begin() as conn:
        sql = """
        SELECT t1.album_id, t1.title, t1.release_date, tracks.track_id, tracks.genre, tracks.title AS track_title, tracks.runtime
        FROM tracks
        JOIN
        (
        SELECT albums.album_id, albums.title, albums.release_date
        FROM albums
        JOIN tracks ON tracks.album_id = albums.album_id
        GROUP BY albums.album_id
        ORDER BY ABS(:avg - AVG(tracks.vibe)), ABS(:num_tracks - COUNT(tracks.track_id))
        LIMIT 1
        ) AS t1 ON t1.album_id = tracks.album_id
        """
        result1 = conn.execute(
            sa.text(sql), [{"avg": avg, "num_tracks": num_tracks}]
        ).fetchall()

        album_id = result1[0][0]
        # genre = max(result1[0][4], key=result1[0][4])
        # print(genre)

        tracks = [{"track_id": t[3], "title": t[4], "runtime": t[5]} for t in result1]

        sql = """
        SELECT artists.artist_id, artists.name
        FROM artists
        JOIN album_artist ON album_artist.artist_id = artists.artist_id
        WHERE album_artist.album_id = :album_id
        """
        result2 = conn.execute(sa.text(sql), [{"album_id": album_id}]).fetchall()

        artists = [{"artist_id": a[0], "name": a[1]} for a in result2]

        album = {
            "album_id": album_id,
            "title": result1[0][1],
            "release_date": result1[0][2],
            "genre_id": result1[0][3],
            "artists": artists,
            "tracks": tracks,
        }

        return album
