from fastapi import FastAPI
from src.api import artists


description = """
Movie API returns dialog statistics on top hollywood movies from decades past.

## Characters

You can:
* **list characters with sorting and filtering options.**
* **retrieve a specific character by id**

## Movies

You can:
* **list movies with sorting and filtering options.**
* **retrieve a specific movie by id**
"""
tags_metadata = [
    {
        "name": "artists",
        "description": "Aceess information on artists.",
    },
    {
        "name": "movies",
        "description": "Access information on top-rated movies.",
    },
    {"name": "lines", "decription": "Acess information on lines in movies."},
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
# app.include_router(movies.router)
# app.include_router(lines.router)
# app.include_router(conversations.router)


@app.get("/")
async def root():
    return {"message": "Welcome to the Rock API. See /docs for more information."}
