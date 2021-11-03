from app import app
from flask import render_template, flash, redirect, url_for, request, jsonify
from app.forms import Login, SignUp
from app.api.database import get_song_metadata, add_song_metadata, add_user
from markupsafe import escape


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


# API Routes
@app.route("/api/song/metadata/<int:song_id>", methods=["GET"])
def get_song_meta(song_id):
    song_meta = get_song_metadata(song_id=song_id)
    return song_meta


@app.route("/api/song/metadata/add", methods=["POST"])
def add_song_meta():
    song_data = request.json
    add_song_metadata(song_info=song_data)

    # @TODO add error handling
    return "done"


@app.route("/api/users/add", methods=["POST"])
def add_new_user():
    user_data = request.json
    add_user(user_info=user_data)

    # @TODO add error handling
    return "done"
