import json
from app import app
from flask import render_template, flash, redirect, url_for, request, Response, session
from app.forms import Login, SignUp
from app.api.database import (
    get_song_metadata,
    add_song_metadata,
    add_user,
    get_user,
    get_all_songs,
    get_user_by_username,
    get_user_by_email
)
# pylint: disable=unused-import
from app.api.spotify import (
    get_track_metadata,
    recommendations_by_artist,
    recommendations_by_genre,
)
# new packages imported
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

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
        try:
            # if it does not fail, it means that the username is already taken
            entity = get_user_by_username(form.username.data)[0]
            flash("Username is not available")
        except IndexError:
            # if not a user found with that username, the username is valid. 
            # we also need to check if the email is valid
            try:
                entity = get_user_by_email(form.email.data)[0]
                flash("Email is not available")
            except IndexError:
                # then username and emal are valid, now we can create the account
                user = {
                    "accountCreated": datetime.now().strftime("%d-%m-%Y %H:%M:%S EST"),
                    "email": form.email.data,
                    "firstName": form.firstName.data,
                    "lastName" : form.lastName.data,
                    "username": form.username.data,
                    "password": generate_password_hash(form.password.data)
                }
                # add user to database
                add_user(user)
                # add user to the session, then redirect him to home
                # I created a new user object so that the password hash is not seen by anyone with access to the session
                session_user = {
                    "email":user['email'],
                    "firstName": user["firstName"],
                    "lastName": user["lastName"],
                    "username":user["username"]
                }
                session["user"] = session_user
                return redirect(url_for("home"))  # User is automatically logged in
    return render_template("signup.html", title="Sign Up", form=form)  # pass form


@app.route("/login", methods=["GET", "POST"])
def login():
    form = Login()  # instantiate object
    if form.validate_on_submit():
        # validate the user, if the username, then it will try to authenticate password
        try:
            entity = get_user_by_username(form.username.data)[0]
            # check if password matches, if then, redirect it to the homepage
            if check_password_hash(entity['password'], form.password.data):
                # user is authenticated
                session_user = {
                "email":entity['email'],
                "firstName": entity["firstName"],
                "lastName": entity["lastName"],
                "username":entity["username"]
                }
                # add user to session
                session["user"] = session_user
                return redirect(url_for("home"))
            else:
                # user is not authenticated flash error message
                raise IndexError # just go to the except
        except IndexError:
            # not an user with that username
            # flash an error message
            flash('Invalid username or password')
    return render_template("login.html", title="Log In", form=form)  # pass form


@app.route("/logout")
def logout():
    return render_template("logout.html", title="Log Out")


@app.route("/home")
def home():
    return render_template("home.html", title="Home", user=session['user']) 

@app.route("/recommendation")
def recommendation():
    return render_template("recommendation.html", title="Recommendation")

@app.route("/liked_songs",methods=["GET","POST"])
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
