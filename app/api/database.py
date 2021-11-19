from google.cloud import datastore
import json
import dotenv
from google.cloud.datastore import query
dotenv.load_dotenv(dotenv.find_dotenv())

import dotenv

dotenv.load_dotenv(dotenv.find_dotenv())
datastore_client = datastore.Client(project="song-recommender-team2")


def add_user(user_info: dict):
    """Add a new user to the users table

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

def get_all_users():
    """Get all users
    
    Returns:
        List[<datastore.Entity>]: List of users
    """
    query = datastore_client.query(kind="users")
    users = list(query.fetch())
    return users

def get_user_by_username(username: str):
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

def get_user_by_email(email: str):
    """Get the user info

    Args:
        email (str): The email of a user, it should be unique

    Returns:
        List[<datastore.Entity>]: The user info
    """
    query = datastore_client.query(kind="users")
    query = query.add_filter("email", "=", email)
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
    """Get a song metadata

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


def get_all_songs():
    """Get all the songs added by a user
        @TODO this function should take a user ID argument and return only songs
        that the current user has added. Right now, it returns all songs in the DB
        which is not a good idea
    Returns:
        List<datastore.Entity>: The user added songs
    """
    query = datastore_client.query(kind="song-metadata")
    results = list(query.fetch())
    all_songs = [dict(song) for song in results]
    return json.dumps(all_songs)
