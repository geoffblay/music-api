from fastapi import APIRouter, HTTPException
from src import database as db, weather
import sqlalchemy as sa
from fastapi.params import Query

router = APIRouter()


@router.get("/albums/", tags=["albums"])
def list_albums(
    name: str = "",
    limit: int = Query(50, ge=1, le=250),
    offset: int = Query(0, ge=0),
):
    """
    This endpoint returns a list of albums. For each album it returns:
    * `album_id`: the unique id of the album
    * `title`: the title of the album
    * `release_date`: the release date of the album
    * `artist_names`: a comma-separated list of artists associated with the album

    You can filter for albums whose titles contain a string by using the
    `name` query parameter.

    The `limit` and `offset` query
    parameters are used for pagination. The `limit` query parameter specifies the
    maximum number of results to return. The `offset` query parameter specifies the
    number of results to skip before returning results.
    """

    list_stmt = sa.text(
        """
        SELECT a.album_id, a.title, a.release_date, ar.name AS artist_names
        FROM albums AS a
        JOIN album_artist AS aa ON aa.album_id = a.album_id
        JOIN artists AS ar ON ar.artist_id = aa.artist_id
        WHERE LOWER(a.title) LIKE '%' || :name || '%'
        LIMIT :limit
        OFFSET :offset
        """
    )

    name = name.lower()

    with db.engine.begin() as conn:
        result = conn.execute(
            list_stmt,
            {
                "name": name,
                "limit": limit,
                "offset": offset,
            },
        )
        result = [r._asdict() for r in list(result)]
    return result


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


def get_score(weather, time, temperature, mood):
    score = 0

    # TEMPERATURE
    score += temperature * 4

    # TIME OF DAY
    if int(time.split(":")[0]) >= 18 or int(time.split(":")[0]) <= 6:
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
        result = conn.execute(sa.text(sql), [{"cond": weather}]).fetchone()
        score += result[0]

    # MOOD
    mood = mood.lower()
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


@router.get("/albums/recommend/", tags=["albums"])
def recommend(
    location: str = "San Luis Obispo",
    mood: str = "Happy",
    num_tracks: int = Query(10, ge=1, le=100),
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

    You can curate the album recommendations by providing the following parameters:
    * `location`: specifying location will return tracks that match the current weather and time in a given location. Location must be a valid city, US zip, or lat,long (decimal degree, e.g: 35.2828,120.6596).
    * `mood`: specifying mood will return an album that match the vibe. Mood must be one of the following:
        - happy
        - party
        - workout
        - focus
        - chill
        - sleep
        - heartbroken
    * `num_tracks`: specifying num_tracks will return an album close to the specified number of tracks.
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

    score = get_score(
        weather_data["weather"], weather_data["time"], weather_data["temperature"], mood
    )

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
        ORDER BY ABS(:score - AVG(tracks.vibe_score)), ABS(:num_tracks - COUNT(tracks.track_id))
        LIMIT 1
        ) AS t1 ON t1.album_id = tracks.album_id
        """
        result1 = conn.execute(
            sa.text(sql), [{"score": score, "num_tracks": num_tracks}]
        ).fetchall()

        album_id = result1[0][0]

        tracks = [{"track_id": t[3], "title": t[5], "runtime": t[6]} for t in result1]

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
