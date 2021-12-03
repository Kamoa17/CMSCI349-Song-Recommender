import dotenv

dotenv.load_dotenv(dotenv.find_dotenv())
config = dotenv.dotenv_values(dotenv.find_dotenv())


class Config(object):
    SECRET_KEY = config.get("SECRET_KEY")
    SPOTIFY_CLIENT_ID = config.get("SPOTIPY_CLIENT_ID") or None
    SPOTIFY_CLIENT_SECRET = config.get("SPOTIPY_CLIENT_SECRET") or None

    # Flask
    FLASK_APP = config.get("FLASK_APP") or "app.py"
    FLASK_ENV = config.get("FLASK_ENV") or "production"

    # Google Cloud API Credentials
    GOOGLE_APPLICATION_CREDENTIALS = (
        config.get("GOOGLE_APPLICATION_CREDENTIALS")
        or "application_default_credentials.json"
    )
