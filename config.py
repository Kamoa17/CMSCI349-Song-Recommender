import os
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY")
    # SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID") or None
    # SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET") or None

    # Flask
    # FLASK_APP = os.environ.get("FLASK_APP") or "app.py"
    # FLASK_ENV = os.environ.get("FLASK_ENV")

    # Google Cloud API Credentials
    #GOOGLE_APPLICATION_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
