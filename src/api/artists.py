from fastapi import APIRouter, HTTPException
from src import database as db
import sqlalchemy as sa

router = APIRouter()


@router.get("/artists/{artist_id}", tags=["artists"])
def get_artist(artist_id: int):
    """
    This endpoint returns a single artist by its identifier. For each artist, the following information is returned:
    * `artist_id`: the internal id of the artist.
    * `name`: the name of the artist.
    * `birthdate`: the birthdate of the artist.
    * `deathdate`: the deathdate of the artist (if applicable).
    * `gender`: the gender of the artist.
    * `tracks`: a list of tracks associated with the artist.
    * `albums`: a list of albums associated with the artist.

    Each track is represented by a dictionary with the following keys:
    * `track_id`: the internal id of the track.
    * `title`: the title of the track.
    * `release_date`: the release date of the track.

    Each album is represented by a dictionary with the following keys:
    * `album_id`: the internal id of the album.
    * `title`: the title of the album.
    * `release_date`: the release date of the album.
    """

    # check if artist_id is an integer
    if not db.try_parse(int, artist_id):
        raise HTTPException(status_code=404, detail="Artist ID must be an integer")

    # get artist and track information for artist
    track_stmt = sa.text(
        """
        SELECT 
            ar.artist_id, ar.name, ar.birthdate, ar.deathdate, ar.gender,
            t.track_id, t.title, t.release_date
        FROM 
            artists AS ar
            JOIN track_artist AS ta ON ar.artist_id = ta.artist_id
            JOIN tracks AS t ON ta.track_id = t.track_id
        WHERE 
            ar.artist_id = :artist_id
        """
    )

    # get artist and album information for artist
    album_stmt = sa.text(
        """
        SELECT 
            a.album_id, a.title AS album_title, a.release_date
        FROM 
            artists AS ar
            JOIN album_artist AS aa ON ar.artist_id = aa.artist_id
            JOIN albums AS a ON aa.album_id = a.album_id
        WHERE 
            ar.artist_id = :artist_id
        """
    )

    with db.engine.begin() as conn:
        # get tracks and albums from database
        track_result = conn.execute(track_stmt, {"artist_id": artist_id})
        if track_result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Artist not found")

        album_result = conn.execute(album_stmt, {"artist_id": artist_id})

        track_result = [row._asdict() for row in track_result]
        album_result = [row._asdict() for row in album_result]

        # Create dictionary to represent artist, will add to tracks and albums later
        artist = {
            "artist_id": track_result[0]["artist_id"],
            "name": track_result[0]["name"],
            "birthdate": track_result[0]["birthdate"],
            "deathdate": track_result[0]["deathdate"],
            "gender": track_result[0]["gender"],
            "tracks": [],
            "albums": [],
        }

        # iterate through each track, add to the artist dictionary
        for row in track_result:
            if {
                "track_id": row["track_id"],
                "title": row["title"],
                "release_date": row["release_date"],
            } not in artist["tracks"]:
                # add track to artist if not already added
                artist["tracks"].append(
                    {
                        "track_id": row["track_id"],
                        "title": row["title"],
                        "release_date": row["release_date"],
                    }
                )

        for row in album_result:
            if {
                "album_id": row["album_id"],
                "title": row["album_title"],
                "release_date": row["release_date"],
            } not in artist["albums"]:
                # add album to artist if not already added
                artist["albums"].append(
                    {
                        "album_id": row["album_id"],
                        "title": row["album_title"],
                        "release_date": row["release_date"],
                    }
                )

        return artist
