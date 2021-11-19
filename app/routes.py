import json
from app import app
from flask import render_template, flash, redirect, url_for, request, Response, session
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from app.forms import Login, SignUp
from app.api.database import (
    get_song_metadata,
    add_song_metadata,
    add_user,
    get_user,
    get_all_songs,
    get_user_by_username,
    get_user_by_email, 
    get_all_users
)
# pylint: disable=unused-import
from app.api.spotify import (
    get_track_metadata,
    recommendations_by_artist,
    recommendations_by_genre,
)
# Models
from app.models.user import User

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# set up flask login
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)
login_manager.login_message = "Login to have access to that page"

@login_manager.user_loader
def load_user(user_id):
    """Load the user information just by ID

    Args: user_id (int): The unique identifier of the user in datastore

    Returns:
        <datastore.Entity>: User info 
    """
    user = get_user(user_id)
    if len(user) != 0:
        return user[0]

@app.route("/")
@app.route("/start")
def start():
    # when the program initiates
    # clear the session
    session.clear()
    return render_template("start.html", title="Start")


@app.route("/signup", methods=["GET", "POST"])
def signup():
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
            firstName= form.firstName.data,
            lastName= form.lastName.data,
            email= form.email.data,
            username= form.username.data,
            password= form.password.data
        )
        # add user to database
        user_dict = user.toDict()
        user_dict["creationDate"] = datetime.now().isoformat()
        add_user(user_dict)
        # login user with flask login
        login_user(user)
        return redirect(url_for("home"))  # User is automatically logged in
    return render_template("signup.html", title="Sign Up", form=form)  # pass form


@app.route("/login", methods=["GET", "POST"])
def login():
    form = Login()  # instantiate object
    if form.validate_on_submit():
        # validate the user, if the username, then it will try to authenticate password
        user = get_user_by_username(form.username.data)
        if len(user) == 0:
            flash("Username not valid")
            return redirect(url_for("login"))
        user = user[0]
        # check if password matches, if then, redirect it to the homepage
        if check_password_hash(user['password'], form.password.data):
            user = User(firstName=user['firstName'],
                        lastName=user['lastName'],
                        email=user['email'],
                        username=user['username'],
                        password=form.password.data
                        )
            # login user with flask login
            login_user(user, remember=True)
            return redirect(url_for("home"))
        else:
            flash("Password is invalid")
            return redirect(url_for("login"))
    return render_template("login.html", title="Log In", form=form)  # pass form


@app.route("/logout")
def logout():
    logout_user()
    return render_template("logout.html", title="Log Out")


@app.route("/home")
#@login_required
def home():
    import pdb;pdb.set_trace()
    return render_template("home.html", title="Home", user=current_user) 

@app.route("/recommendation")
@login_required
def recommendation():
    return render_template("recommendation.html", title="Recommendation")

@app.route("/liked_songs",methods=["GET","POST"])
@login_required
def liked_songs():
    # for future backend:
    # retrieve songs from liked songs from the user
    # transform the data back into something to present
    return render_template("liked_songs.html", title="Liked Songs")


@app.route("/account")
def user_account():
    # user = get_user() 
    return "Account Page"
    #return render_template("account.html")


@app.route("/songs")
def user_songs():
    return render_template("songs.html")


# API Routes
@app.route("/api/song/metadata/<int:song_id>", methods=["GET"])
@app.route("/song/<int:song_id>")
def get_song_meta(song_id):
    song_meta = get_song_metadata(song_id=song_id)
    return song_meta


@app.route("/api/songs/list")
@app.route("/songs/list")
def list_all_songs():
    all_songs = get_all_songs()
    if "/api/" in request.url_rule.rule:
        r = Response(all_songs, 200, mimetype="application/json")
        r.headers["Content-Type"] = "application/json;;charset=iso-8859-1"
        return r
    return render_template("songs.html", title="Liked Songs", data=json.loads(all_songs))


@app.route("/api/song/metadata/add/<track_id>", methods=["POST"])
def add_song_meta(track_id):

    song_data = request.json
    add_song_metadata(song_info=song_data)

    # @TODO add error handling
    return "done"


@app.route("/api/users/add", methods=["POST"])
@app.route("/add-user", methods=["POST", "GET"])
def add_new_user():
    if request.method == "POST":
        user_data = request.json
        add_user(user_info=user_data)

        # @TODO add error handling
        return "done"
    # return render_template("")
    return "done"
