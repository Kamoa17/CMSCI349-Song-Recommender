from typing import Any, List
import dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

dotenv.load_dotenv(dotenv.find_dotenv())

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())


def parse_track_info(track_info: dict):
    """Helper function to parse track information and return only the information that we need

    Args:
        track_info (dict): Track information returned from the Spotify API

    Returns:
        dict: A key, value map of useful track information
    """
    assert isinstance(track_info, dict)
    parsed_track_info = {
        # Track information
        "track_id": track_info["id"],
        "track_name": track_info["name"],
        "track_duration_ms": track_info["duration_ms"],
        "track_url": track_info["external_urls"]["spotify"],
        # Artist information
        # Note: a song can have multiple artists, so account for that
        "artists": [artist["name"] for artist in track_info["artists"]],
        # Album information
        "album_name": track_info["album"]["name"],
        "album_cover_image_url": track_info["album"]["images"][0]["url"],
        "album_release_date": track_info["album"]["release_date"],
    }
    return parsed_track_info


def get_track_metadata(track_id: Any) -> dict:
    """Get the metadata of a track from the track id

    Args:
        track_id (Any): The Spotify track ID

    Returns:
        dict: A track track's metadata
    """
    track = spotify.track(track_id=track_id)
    song_metadata = parse_track_info(track)

    return song_metadata


def parse_recommendations(recommendations: List[dict]) -> list:
    """Parse recommendations to return only information we are interested in

    Args:
        recommendations (dict): Recommanded songs based on spotify API
    
    Returns:
        list: A list of parse recommendations
    """
    parsed_recommendations = []
    for recommended_track in recommendations["tracks"]:
        parsed_recommendations.append(parse_track_info(recommended_track))

    return parsed_recommendations


def recommendations_by_artist(seed_artists_ids: list, number_of_recs: int = 10) -> list:
    """Get song recommendations based on an artists. If multiple artists are passed, recommendations will
    be based on the various artists

    Args:
        seed_artists_ids (list): List of artists to use for seeding recommendations.
        number_of_recs (int, optional): Number of recommendations to return. Defaults to 10.

    Returns:
        list: A list of songs
    """
    if isinstance(seed_artists_ids, str):
        recommanded_songs = spotify.recommendations(
            seed_artists=[seed_artists_ids], limit=number_of_recs
        )
        return recommanded_songs
    recommanded_songs = spotify.recommendations(
        seed_artists=seed_artists_ids, limit=number_of_recs
    )
    return parse_recommendations(recommanded_songs)


def recommendations_by_genre(seed_genre: str, number_of_recs: int = 10) -> list:
    """Get song recommendations based on an artists. If multiple artists are passed, recommendations will
    be based on the various artists

    Args:
        seed_artists_ids (list): List of artists to use for seeding recommendations.
        number_of_recs (int, optional): Number of recommendations to return. Defaults to 10.

    Returns:
        list: A list of songs
    """
    seed_genre = seed_genre.lower()
    recommended_songs = spotify.recommendations(seed_genres=[seed_genre], limit=number_of_recs)
    return parse_recommendations(recommended_songs)


def get_new_releases(country: str = "US", limit: int = 24) -> list:
    """Get newly released songs on Spotify

    Args:
        country (str, optional): The two letter country code. Defaults to "US".
        limit (int, optional): Number of releases to return. Defaults to 24.

    Returns:
        list: A list of newly released songs
    """
    spotify_new_releases = spotify.new_releases(country=country, limit=limit)
    all_releases = []
    for release in spotify_new_releases.get("albums").get("items"):
        # remove the available_markets data since we don't really need it
        release.pop("available_markets")
        all_releases.append(release)
        #all_releases[release.get("id")] = release
    return all_releases
