from flask import Flask
from config import Config


app = Flask(__name__, static_folder="../static")
app.config.from_object(Config)  # read and apply
# app.env = Config.FLASK_ENV
# app.debug = True

from app import routes
