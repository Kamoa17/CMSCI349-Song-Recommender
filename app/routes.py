import json
import logging
from datetime import datetime
from typing import List

from flask import Response, flash, redirect, render_template, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from google.cloud import datastore
from werkzeug.security import check_password_hash

from app import app
from app.api.database import (
    add_song_metadata,
    add_user,
    get_all_songs,
    get_song_metadata,
    get_user,
    get_user_by_email,
    get_user_by_username,
)

from app.api.spotify import (
    get_new_releases,
    get_track_metadata,
    recommendations_by_genre,
)
from app.forms import Login, SignUp

# Models
from app.models.user import User

# set up flask login
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)
login_manager.login_message = "Login to have access to that page"


@login_manager.user_loader
def load_user(user_id: int) -> List[datastore.Entity]:
    """Load the user information just by ID

    Args: user_id (int): The unique identifier of the user in datastore

    Returns:
        <datastore.Entity>: User info
    """
    user = get_user(int(user_id))
    if len(user) > 0:
        user_entity = user[0]
        user = User(
            firstname=user_entity["firstname"],
            lastname=user_entity["lastname"],
            email=user_entity["email"],
            username=user_entity["username"],
            password=user_entity["password"],
        )
        return user


@app.route("/api/signup")
@app.route("/signup", methods=["GET", "POST"])
def signup() -> Response:
    """Sing up route. This route adds tha new user to the user database

    Returns:
        Response: Returns the sign-up page template or redirects the user
                to the sign up page if the user is not aviailable
    """
    form = SignUp()  # instantiate object
    if form.validate_on_submit():
        # validate if username is available
        entity = get_user_by_username(form.username.data)
        print(entity)
        # if the response is not empty, means that the username is not available
        if len(entity) != 0:
            flash("Username is not available")
            return redirect(url_for("signup"))

        # checking if email is valid
        entity = get_user_by_email(form.email.data)
        if len(entity) != 0:
            flash("Email is not available")
            return redirect(url_for("signup"))

        # if anything was returned before, then the user is valid
        # create user model
        user = User(
            firstname=form.firstName.data,
            lastname=form.lastName.data,
            email=form.email.data,
            username=form.username.data,
            password=form.password.data,
        )
        # add user to database
        user_dict = vars(user)
        user_dict["creation_date"] = datetime.now().isoformat()
        user_dict["password"] = user.hash_password()
        add_user(user_dict)
        # login user with flask login
        login_user(user)
        return redirect(url_for("home"))  # User is automatically logged in
    return render_template("signup.html", title="Sign Up", form=form)  # pass form


@app.route("/api/login")
@app.route("/login", methods=["GET", "POST"])
def login() -> Response:
    """Log in route. This route handles user logins

    Returns:
        Response: Returns the login page template or redirects the user
                    to the login page if the user is not aviailable
    """
    form = Login()  # instantiate object
    if "/api/" in request.url_rule.rule:
        form_data = request.form
        username = form_data["username"]
        password = form_data["password"]
        user = get_user_by_username(username)[0]
        if check_password_hash(user["password"], password):
            user = User(
                user["firstname"],
                user["lastname"],
                user["email"],
                user["username"],
                password,
            )
            login_user(user)
            return "User logged in"
        return "None"

    if form.validate_on_submit():
        # validate the user, if the username, then it will try to authenticate password
        user = get_user_by_username(form.username.data)
        if len(user) == 0:
            flash("Username not valid")
            return redirect(url_for("login"))
        user = user[0]
        # check if password matches, if then, redirect it to the homepage
        if check_password_hash(user["password"], form.password.data):
            user = User(
                firstname=user["firstname"],
                lastname=user["lastname"],
                email=user["email"],
                username=user["username"],
                password=form.password.data,
            )
            # login user with flask login
            login_user(user, remember=True)
            return redirect(url_for("home"))
        else:
            flash("Password is invalid")
            return redirect(url_for("login"))
    return render_template("login.html", title="Log In", form=form)  # pass form


@app.route("/api/logout")
@app.route("/logout")
@login_required
def logout() -> Response:
    """Log out the user, destroying the session information

    Returns:
        Response: The logout page
    """
    logout_user()
    return redirect("/")


@app.route("/home")
@app.route("/")
def home() -> Response:
    """The Homepage route

    Returns:
        Response: A rendered template of the home page
    """
    recommendations_data = recommendations_by_genre(seed_genre="pop", number_of_recs=21)
    new_releases = get_new_releases()
    return render_template(
        "home.html",
        title="Home",
        recommendations_data=recommendations_data,
        new_release_data=new_releases,
    )


@app.route("/api/account")
@app.route("/account")
@login_required
def user_account() -> Response:
    """The User Account route

    Returns:
        Response: The rendered user account page
    """
    return render_template("account.html", title="Account")


@app.route("/api/songs")
@app.route("/songs")
@login_required
def songs() -> Response:
    """The user's Song Library page

    Returns:
        Response: The user's song page
    """
    user_id = current_user.get_id()
    if not isinstance(user_id, int):
        user_id = int(user_id)

    all_songs = get_all_songs(user_id=user_id)
    if "/api/" in request.url_rule.rule:
        response = Response(all_songs, 200, mimetype="application/json")
        response.headers["Content-Type"] = "application/json;;charset=iso-8859-1"
        return response
    return render_template(
        "songs.html", title="Liked Songs", data=json.loads(all_songs)
    )


# Other API Routes
@app.route("/api/song/metadata/<int:song_id>", methods=["GET"])
@app.route("/song/<int:song_id>")
@login_required
def get_song_meta(song_id: str) -> Response:
    """Get the metadata of a particular song

    Args:
        song_id (str): The song's ID

    Returns:
        Response: A json string with the song metadata
    """
    song_meta = get_song_metadata(song_id=song_id)
    return song_meta


@app.route("/api/song/metadata/add/<track_id>", methods=["POST"])
@login_required
def add_song_meta(track_id: str) -> Response:
    """Adds a new song to the user's song collection

    Args:
        track_id (str): The song's ID

    Returns:
        Response: A json response object

    """
    response = Response(
        json.dumps({"response": 200, "message": "Song added"}),
        200,
        mimetype="application/json",
    )
    response.headers["Content-Type"] = "application/json;;charset=iso-8859-1"
    try:
        song_data = get_track_metadata(track_id=track_id)
        song_data["user_id"] = current_user.get_id()
        add_song_metadata(song_info=song_data)

    except Exception as ex:
        logging.exception(ex)
        response = Response(
            json.dumps(
                {"response": 500, "message": "An error occurred while adding the song"}
            ),
            status=500,
            mimetype="application/json",
        )
    return response


@app.route("/api/recommendations", methods=["POST"])
@login_required
def recommendations():
    """Get song recommendations

    Returns:
        Response: A json list of recommended songs based on user input
    """
    user_form = request.json
    seed_genre = user_form["genre"]
    recommendations_data = recommendations_by_genre(
        seed_genre=seed_genre, number_of_recs=21
    )
    return json.dumps(recommendations_data)
