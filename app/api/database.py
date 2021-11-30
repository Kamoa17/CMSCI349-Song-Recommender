import json

import dotenv
from google.cloud import datastore

dotenv.load_dotenv(dotenv.find_dotenv())
datastore_client = datastore.Client(project="song-recommender-team2")


def add_user(user_info: dict) -> None:
    """Add a new user to the users table

    Args:
        user_info (dict): A key, value mapping of the user attributes
    """
    entity = datastore.Entity(key=datastore_client.key("users"))
    entity.update(user_info)
    datastore_client.put(entity)


def get_user(user_id: int) -> list:
    """Get the user info

    Args:
        user_id (int): The unique identifier of the user

    Returns:
        List[<datastore.Entity>]: The user info
    """
    query = datastore_client.query(kind="users")
    query_key = datastore_client.key("users", user_id)
    query = query.add_filter("__key__", "=", query_key)
    user = list(query.fetch())
    return user


def get_all_users() -> list:
    """Get all users

    Returns:
        List[<datastore.Entity>]: List of users
    """
    query = datastore_client.query(kind="users")
    users = list(query.fetch())
    return users


def get_user_by_username(username: str) -> list:
    """Get the user info

    Args:
        username (str): The username of a user, it should be unique

    Returns:
        List[<datastore.Entity>]: The user info
    """
    query = datastore_client.query(kind="users")
    query = query.add_filter("username", "=", username)
    user = list(query.fetch())
    return user


def get_user_by_email(email: str) -> list:
    """Get the user info

    Args:
        email (str): The email of a user, it should be unique

    Returns:
        list: The user information as a list
    """
    query = datastore_client.query(kind="users")
    query = query.add_filter("email", "=", email)
    user = list(query.fetch())
    return user


def add_song_metadata(song_info: dict) -> None:
    """Add a new song metadata

    Args:
        song_info (dict): Song metadata information
    """
    entity = datastore.Entity(key=datastore_client.key("song-metadata"))
    entity.update(song_info)
    datastore_client.put(entity)


def get_song_metadata(song_id: int) -> str:
    """Get a song metadata

    Args:
        song_id (int): The unique ID of the song

    Returns:
        str: A json object of the user information
    """
    query = datastore_client.query(kind="song-metadata")
    song_key = datastore_client.key("song-metadata", song_id)
    query = query.add_filter("__key__", "=", song_key)
    results = list(query.fetch())
    return json.dumps(dict(results[0]))


def get_all_songs(user_id: int) -> str:
    """Get all the songs added by a user

    Args:
        user_id (int): The current user's ID

    Returns:
        str: A json object of the user's added songs
    """
    query = datastore_client.query(kind="song-metadata")
    query = query.add_filter("user_id", "=", user_id)
    results = list(query.fetch())
    all_songs = [dict(song) for song in results]
    return json.dumps(all_songs)
