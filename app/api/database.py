from google.cloud import datastore
import json

import dotenv

dotenv.load_dotenv("../../.env")
datastore_client = datastore.Client(project="song-recommender-team2")


def add_user(user_info: dict):
    """Adds a new user to th users table

    Args:
        user_info (dict): A key, value mapping of the user attributes
    """
    entity = datastore.Entity(key=datastore_client.key("users"))
    entity.update(user_info)
    datastore_client.put(entity)


def get_user(user_id: int):
    """Get the user info

    Args:
        user_id (int): The unique identifier of the user

    Returns:
        List[<datastore.Entity>]: The user info
    """
    query = datastore_client.query(kind="users")
    query = query.add_filter("id", "=", user_id)
    user = list(query.fetch())
    return user


def add_song_metadata(song_info: dict):
    """Add a new song metadata

    Args:
        song_info (dict): Song metadata information
    """
    entity = datastore.Entity(key=datastore_client.key("song-metadata"))
    entity.update(song_info)
    datastore_client.put(entity)


def get_song_metadata(song_id: int):
    """Gets a song metadata

    Args:
        song_id (int): The unique ID of the song

    Returns:
        List[<datastore.Entity>]: The user info
    """
    query = datastore_client.query(kind="song-metadata")
    song_key = datastore_client.key("song-metadata", song_id)
    query = query.add_filter("__key__", "=", song_key)
    results = list(query.fetch())
    return json.dumps(dict(results[0]))
