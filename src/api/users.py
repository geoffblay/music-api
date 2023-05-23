from fastapi import APIRouter, HTTPException
from src import database as db
from pydantic import BaseModel
import sqlalchemy as sa
from fastapi.params import Query

router = APIRouter()


class UserJson(BaseModel):
    username: str
    password: str


@router.post("/users", tags=["users"])
def add_user(user: UserJson):
    """
    This endpoint adds a user to the database. The following information is required:
    * `username`: the username of the user - must be larger than four characters.
    * `password`: the password of the user - must be larger than eight characters.

    This endpoint returns the following information:
    * `user_id`: the internal id of the user.
    """

    if not db.try_parse(str, user.username):
        raise HTTPException(status_code=422, detail="Username input is invalid.")

    if not db.try_parse(str, user.password):
        raise HTTPException(status_code=422, detail="Password input is invalid.")

    if len(user.password) < 8 or len(user.password) > 72:
        raise HTTPException(
            status_code=422,
            detail="Password must be at least 8 characters long and less than 72 characters long.",
        )

    if len(user.username) < 4 or len(user.username) > 32:
        raise HTTPException(
            status_code=422,
            detail="Username must be at least 4 characters long and less than 32 characters long.",
        )

    # set username to lowercase
    user.username = user.username.lower()

    # check if username already exists statement
    check_user_stmt = sa.text(
        """
        SELECT users.username 
        FROM users
        WHERE users.username = :username
        """
    )

    insert_stmt = sa.text(
        """
        INSERT INTO users (username, password)
        VALUES (:username, crypt(:password, gen_salt('bf')))
        RETURNING user_id
        """
    )

    with db.engine.begin() as conn:
        result = conn.execute(check_user_stmt, {"username": user.username})
        if result.first() != None:
            raise HTTPException(status_code=400, detail="Username already exists.")

        result = conn.execute(
            insert_stmt, {"username": user.username, "password": user.password}
        )

    return result.scalar()


@router.post("/users/validate", tags=["users"])
def validate_user(user: UserJson):
    """
    This endpoint validates a user to the database. The following information is required:
    * `username`: the username of the user.
    * `password`: the password of the user.

    This endpoint returns True if the user is valid.
    """

    if not db.try_parse(str, user.username):
        raise HTTPException(status_code=422, detail="Username input is invalid.")

    if not db.try_parse(str, user.password):
        raise HTTPException(status_code=422, detail="Password input is invalid.")

    # set username to lowercase
    user.username = user.username.lower()

    # check if username and password are valid statement
    check_user_stmt = sa.text(
        """
        SELECT user_id
        FROM users
        WHERE username = :username AND password = crypt(:password, password)
        """
    )

    with db.engine.begin() as conn:
        result = conn.execute(
            check_user_stmt, {"username": user.username, "password": user.password}
        )
        if result.first() == None:
            raise HTTPException(
                status_code=400, detail="Username or password is incorrect."
            )

    return True
