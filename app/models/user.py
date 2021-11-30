from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from google.cloud import datastore
import dotenv
from app.api.database import get_user_by_username, get_user # pylint: disable=import-error

dotenv.load_dotenv(dotenv.find_dotenv())
datastore_client = datastore.Client(project="song-recommender-team2")


class User(UserMixin):
    def __init__(
        self, firstname: str, lastname: str, email: str, username: str, password: str
    ) -> None:
        """The user class which holds information about the current user

        Args:
            firstName (str): The user's first name
            lastName (str): The user's last name
            email (str): A unique email for the user
            username (str): A unique username for the user
            password (str): The user's password
        """
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.username = username
        self.password = password

    def hash_password(self) -> str:
        """Hash the user password

        Returns:
            str: The hasshed password using the default specified method
        """
        return generate_password_hash(self.password)

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def is_active(self) -> bool:
        return True

    def get_id(self) -> int:
        """Get the User's ID

        Returns:
            int: The user's ID
        """
        user = get_user_by_username(self.username)
        if len(user) != 0:
            user_id = user[0].id
            return user_id
        return -1

    def get_user(self, user_id) -> list:
        """Get the user info

        Returns:
            List[<datastore.Entity>]: The user info
        """
        if not isinstance(user_id, int):
            user_id = int(user_id)
        return get_user(user_id=user_id)
