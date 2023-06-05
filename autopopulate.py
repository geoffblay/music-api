from faker import Faker
from src import database as db
import os
import dotenv
import sqlalchemy

fake = Faker()

"""
Note: Due to the interdependencies between Artist, Album, and Track, we need to insert them in a specific order
This slows down the process, but it's the only way to ensure that the data is inserted correctly
Users and 
"""


def database_connection_url():
    dotenv.load_dotenv()
    DB_USER: str = os.environ.get("POSTGRES_USER")
    DB_PASSWD = os.environ.get("POSTGRES_PASSWORD")
    DB_SERVER: str = os.environ.get("POSTGRES_SERVER")
    DB_PORT: str = os.environ.get("POSTGRES_PORT")
    DB_NAME: str = os.environ.get("POSTGRES_DB")
    return f"postgresql://{DB_USER}:{DB_PASSWD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"


engine = sqlalchemy.create_engine(database_connection_url(), use_insertmanyvalues=True)

num_artists = 400
num_users = 10000
num_playlists = 14000
num_tracks_in_playlists = 1000000

genres = ["rock", "pop", "rap", "country", "jazz", "classical", "metal", "hip-hop"]


def seed_db(engine):
    with engine.begin() as connection:
        first_track_id, last_track_id = add_music_data(connection)
        first_user_id, last_user_id = add_user_data(connection)
        add_playlists(
            connection, first_user_id, last_user_id, first_track_id, last_track_id
        )


# due to the interdependencies between Artist, Album, and Track, we need to insert them in a specific order
# This slows down the process, but it's the only way to ensure that the data is inserted correctly
def add_music_data(connection):
    firstTrackFlag = True
    for _ in range(num_artists):
        if _ % 10 == 0:
            print("Artist #" + str(_) + " created")

        # create an artist, 1 in 5 artists will have a deathdate
        if fake.random_int(min=0, max=4) == 0:
            deathdate = fake.date_between(start_date="-100y", end_date="today")
        else:
            deathdate = None
        artist_data = {
            "name": fake.name(),
            "gender": fake.random_element(elements=("M", "F", None)),
            "birthdate": fake.date_of_birth(),
            "deathdate": deathdate,
        }
        result = connection.execute(sqlalchemy.insert(db.artists), artist_data)
        artist_id = result.inserted_primary_key[0]

        # Create 5-10 albums per previously created artist
        for _ in range(fake.random_int(min=5, max=10)):
            album_data = {
                "title": fake.sentence(nb_words=fake.random_int(min=1, max=5))
                .strip(".")
                .title(),
                "release_date": fake.date_between(start_date="-50y", end_date="today"),
            }
            result = connection.execute(sqlalchemy.insert(db.albums), album_data)
            album_id = result.inserted_primary_key[0]

            # Create association between artist and album
            album_artist_data = {
                "album_id": album_id,
                "artist_id": artist_id,
            }
            connection.execute(sqlalchemy.insert(db.album_artist), album_artist_data)
            album_genre = genres[fake.random_int(min=0, max=len(genres) - 1)]
            # Create 6-10 tracks per album
            for _ in range(fake.random_int(min=6, max=10)):
                track_data = {
                    "title": fake.sentence(nb_words=fake.random_int(min=1, max=5))
                    .strip(".")
                    .title(),
                    "runtime": fake.random_int(min=90, max=600),
                    "genre": album_genre,
                    "album_id": album_id,
                    "release_date": fake.date_between(
                        start_date=album_data["release_date"], end_date="today"
                    ),
                    "vibe_score": fake.random_int(min=0, max=400),
                }
                result = connection.execute(sqlalchemy.insert(db.tracks), track_data)
                track_id = result.inserted_primary_key[0]

                if firstTrackFlag == True:
                    firstTrackFlag = False
                    firstTrackId = track_id

                # Create association between artist and track
                track_artist_data = {
                    "track_id": track_id,
                    "artist_id": artist_id,
                }
                connection.execute(
                    sqlalchemy.insert(db.track_artist), track_artist_data
                )
    lastTrackId = track_id

    return firstTrackId, lastTrackId


# 3 inserts instead of 100
def add_user_data(connection):
    first_user_data = {"username": fake.user_name(), "password": fake.password()}
    result = connection.execute(sqlalchemy.insert(db.users), first_user_data)
    firstUserId = result.inserted_primary_key[0]

    user_data = [
        {
            "username": fake.user_name(),
            "password": fake.password(),
        }
        for _ in range(num_users - 2)
    ]
    result = connection.execute(sqlalchemy.insert(db.users), user_data)

    last_user_data = {"username": fake.user_name(), "password": fake.password()}
    result = connection.execute(sqlalchemy.insert(db.users), last_user_data)
    lastUserId = result.inserted_primary_key[0]

    lastUserId = result.inserted_primary_key[0]
    print("Users created")
    return firstUserId, lastUserId


# bulk inserting playlists, then bulk inserting playlist_track
def add_playlists(connection, firstUserId, lastUserId, firstTrackId, lastTrackId):
    # create playlists
    playlist_data = [
        {
            "name": fake.sentence(nb_words=fake.random_int(min=1, max=5))
            .strip(".")
            .title(),
            "user_id": fake.random_int(min=firstUserId, max=lastUserId),
        }
        for _ in range(num_playlists)
    ]
    # insert first playlist and retrieve its id
    first_playlist_id = connection.execute(
        sqlalchemy.insert(db.playlists), playlist_data[0]
    ).inserted_primary_key[0]

    # insert the rest of the playlists
    connection.execute(sqlalchemy.insert(db.playlists), playlist_data[1:-1])

    # get the last playlist id
    last_playlist_id = connection.execute(
        sqlalchemy.insert(db.playlists), playlist_data[-1]
    ).inserted_primary_key[0]

    # create associations between playlists and tracks, 5-150 tracks per playlist
    playlist_track_data = [
        {
            "playlist_id": fake.random_int(min=first_playlist_id, max=last_playlist_id),
            "track_id": fake.random_int(min=firstTrackId, max=lastTrackId),
        }
        for _ in range(num_tracks_in_playlists)
    ]

    print("Playlists created in memory - inserting into database")

    # insert all values at once
    connection.execute(sqlalchemy.insert(db.playlist_track), playlist_track_data)
    print("Playlists created")


def main():
    seed_db(engine)


if __name__ == "__main__":
    main()
