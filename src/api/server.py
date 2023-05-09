from fastapi import FastAPI
from src.api import artists, tracks, subgenres, albums, playlists, search


description = """
ROCK API returns information on popular rock artists, albums, and tracks.
"""
tags_metadata = [
    {
        "name": "artists",
        "description": "Aceess information on artists.",
    },
    {
        "name": "albums",
        "decription": "Acess information on albums.",
    },
    {
        "name": "tracks",
        "description": "Access information on tracks.",
    },
    {
        "subgenres": "subgenres",
        "description": "Access information on subgenres.",
    },
    {
        "playlists": "playlists",
        "description": "Access information on playlists.",
    },
    {
        "search": "search",
        "description": "Search for artists, albums, and tracks.",
    },
]

app = FastAPI(
    title="Rock API",
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

app.include_router(artists.router)
app.include_router(albums.router)
app.include_router(playlists.router)

app.include_router(tracks.router)
app.include_router(subgenres.router)
app.include_router(playlists.router)
app.include_router(search.router)


@app.get("/")
async def root():
    return {"message": "Welcome to the Rock API. See /docs for more information."}
