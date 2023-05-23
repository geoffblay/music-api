from sqlalchemy.orm import Session
import src.database as db
from src.datatypes import Albums, Artists, Tracks, Album_Artist, Track_Artist
from faker import Faker
from sqlalchemy import insert

fake = Faker()


def seed_db(engine):
    # start a new connection
    with engine.begin() as connection:
        for _ in range(10):  # Create 50 artists
            artist_data = {
                "name": fake.name(),
                "gender": fake.random_element(elements=("Male", "Female")),
                "birthdate": fake.date_of_birth(),
                "deathdate": fake.date_between(start_date="-100y", end_date="today"),
            }
            result = connection.execute(insert(db.artists), artist_data)
            artist_id = result.inserted_primary_key[
                0
            ]  # get the id of the created artist

            # Create 10 albums per artist
            for _ in range(5):
                album_data = {
                    "title": fake.sentence(nb_words=5),
                    "release_date": fake.date_between(
                        start_date="-10y", end_date="today"
                    ),
                }
                result = connection.execute(insert(db.albums), album_data)
                album_id = result.inserted_primary_key[
                    0
                ]  # get the id of the created album

                # Create association between artist and album
                album_artist_data = {
                    "album_id": album_id,
                    "artist_id": artist_id,
                }
                connection.execute(insert(db.album_artist), album_artist_data)

                # Create 6 tracks per album
                for _ in range(6):
                    track_data = {
                        "title": fake.sentence(nb_words=3),
                        "runtime": fake.random_int(
                            min=120, max=600
                        ),  # between 2 minutes and 10 minutes
                        "genre": fake.word(),
                        "album_id": album_id,
                        "release_date": fake.date_between(
                            start_date=album_data["release_date"], end_date="today"
                        ),
                        "vibe_score": fake.random_int(
                            min=0, max=400
                        ),  # random vibe score between 1 and 10
                    }
                    result = connection.execute(insert(db.tracks), track_data)
                    track_id = result.inserted_primary_key[
                        0
                    ]  # get the id of the created track

                    # Create association between artist and track
                    track_artist_data = {
                        "track_id": track_id,
                        "artist_id": artist_id,
                    }
                    connection.execute(insert(db.track_artist), track_artist_data)


def main():
    seed_db(db.engine)


if __name__ == "__main__":
    main()
