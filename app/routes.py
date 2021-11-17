import json
from app import app
from flask import render_template, flash, redirect, url_for, request, Response
from app.forms import Login, SignUp
from app.api.database import (
    get_song_metadata,
    add_song_metadata,
    add_user,
    get_user,
    get_all_songs,
)
# pylint: disable=unused-import
from app.api.spotify import (
    get_track_metadata,
    recommendations_by_artist,
    recommendations_by_genre,
)


@app.route("/")
@app.route("/start")
def start():
    return render_template("start.html", title="Start")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignUp()  # instantiate object
    if form.validate_on_submit():
        flash(
            "Email: {} | User ID: {} | Password: {}".format(
                form.email.data, form.username.data, form.password.data
            )
        )
        # flash to display messages for prototype, driver
        return redirect(url_for("home"))  # navigation when complete
    return render_template("signup.html", title="Sign Up", form=form)  # pass form


@app.route("/login", methods=["GET", "POST"])
def login():
    form = Login()  # instantiate object
    if form.validate_on_submit():
        flash(
            "User ID: {} | Password: {}".format(form.username.data, form.password.data)
        )
        # flash to display messages for prototype, driver
        return redirect(url_for("home"))  # navigation when complete
    return render_template("login.html", title="Log In", form=form)  # pass form


@app.route("/logout")
def logout():
    return render_template("logout.html", title="Log Out")


@app.route("/home")
def home():
    return render_template("home.html", title="Home")

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
    return render_template("account.html", title="Account")


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
