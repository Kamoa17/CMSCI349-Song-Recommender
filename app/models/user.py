from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from google.cloud import datastore
import dotenv
from app.api.database import add_user, get_user_by_username

dotenv.load_dotenv(dotenv.find_dotenv())
datastore_client = datastore.Client(project="song-recommender-team2")


class User(UserMixin):

    def __init__(self, firstName, lastName, email, username, password) -> None:
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.username = username
        self.hashed_password = generate_password_hash(password)
        
    def toDict(self):
        return {
            "firstName" : self.firstName,
            "lastName" : self.lastName,
            "username" : self.username,
            "email" : self.email,
            "password":self.hashed_password
        }

    def check_hashed_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def get_id(self):
        user = get_user_by_username(self.username)
        if len(user) != 0:
            user_id = user[0].id
            return user_id

    def get_user(self):
        """Get the user info

        Returns:
            List[<datastore.Entity>]: The user info
        """
        query = datastore_client.query(kind="users")
        query = query.add_filter("id", "=", self.user_id)
        user = list(query.fetch())
        return user