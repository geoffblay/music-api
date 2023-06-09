from fastapi import FastAPI
from src.api import artists, tracks, albums, playlists, users


description = """
ROCK API returns information on popular rock artists, albums, and tracks.
"""
tags_metadata = [
    {
        "name": "artists",
        "description": "Access information on artists.",
    },
    {
        "name": "albums",
        "decription": "Access information on albums.",
    },
    {
        "name": "tracks",
        "description": "Access information on tracks.",
    },
    {
        "name": "playlists",
        "description": "Access information on playlists.",
    },
    {
        "name": "users",
        "descritpion": "Add users to the database.",
    },
]

app = FastAPI(
    title="Music API",
    description=description,
    version="0.0.1",
    contact={
        "name": "Geoff Blaylock",
        "email": "blaylock@calpoly.edu",
        "name": "Cole Robinson",
        "email": "crobin27@calpoly.edu",
    },
    openapi_tags=tags_metadata,
)


@app.get("/")
async def root():
    return {"message": "Welcome to the Music API. See /docs for more information."}


app.include_router(artists.router)
app.include_router(albums.router)
app.include_router(playlists.router)
app.include_router(tracks.router)
app.include_router(users.router)
