import os
import json
from flask import Flask, render_template, request, session, redirect, url_for


from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.secret_key = os.getenv("SESSION_KEY")

app.url_map.strict_slashes = False
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{table}".format(
    user=os.getenv("POSTGRES_USER"),
    passwd=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    port=5432,
    table=os.getenv("POSTGRES_DB"),
)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class UserModel(db.Model):
    __tablename__ = "users"

    username = db.Column(db.String(), primary_key=True)
    password = db.Column(db.String())

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<User {self.username}>"


class SongModel(db.Model):
    __tablename__ = "songs"

    name = db.Column(db.String(), primary_key=True)
    data = db.Column(db.PickleType())

    def __init__(self, name, data):
        self.name = name
        self.data = data

    def __repr__(self):
        return f"<Song {self.name}> {self.data}"


# game


@app.route("/")
@app.route("/play/")
def index():
    if "username" not in session:
        session["username"] = ""
    # songs = [song.name for song in SongModel.query.all()]
    # return render_template("modules.html", username=session["username"], songs=songs)
    # return render_template("modules.html", username=session["username"])
    return render_template("play.html")


@app.route("/play/<song_name>")
def play(song_name):
    if "username" not in session:
        session["username"] = ""
    return render_template(
        "play.html", username=session["username"], song_name=song_name
    )


@app.route("/api/<song_name>")
def api(song_name):
    song = SongModel.query.filter_by(name=song_name).first()
    if song is None:
        return None, 418
    return song.data


@app.route("/admin/", methods=("GET", "POST"))
def admin():
    if request.method == "POST":
        if request.form.get("add") is not None:
            name = request.form.get("name")
            info = request.form.get("json")
            error = None
            if not name:
                error = "Please enter song name."
            elif not info:
                error = "Please enter song info."
            else:
                try:
                    json.loads(info)
                except json.JSONDecodeError:
                    error = "Invalid JSON -- please check syntax."
            if error is None:
                song = SongModel(name, info)
                db.session.add(song)
                db.session.commit()
                return redirect(url_for("admin"))
            else:
                return error + ' <br> <a href="/admin/">back</a>', 418

        elif request.form.get("del") is not None:
            songs = [
                SongModel.query.filter_by(name=name).first()
                for name in request.form
                if request.form[name] == "on"
            ]
            for song in songs:
                db.session.delete(song)
            db.session.commit()
            return redirect(url_for("admin"))
        else:
            return "POST request with bad values.  Stop that!"

    else:
        if "username" not in session:
            session["username"] = ""
        songs = [song.name for song in SongModel.query.all()]
        return render_template("admin.html", username=session["username"], songs=songs)


# user settings


@app.route("/user/", methods=("POST", "GET"))
def user():
    if request.method == "POST":
        user = UserModel.query.filter_by(username=session["username"]).first()
        if request.form.get("changepw") is not None:
            old_pw = request.form.get("old_pw")
            new_pw = request.form.get("new_pw")
            error = None

            if old_pw is None:
                error = "Please enter your old password."
            if new_pw is None:
                error = "Please enter your new password."

            if not check_password_hash(user.password, old_pw):
                error = "Old password invalid; please try again."
            if error is None:
                user.password = generate_password_hash(new_pw)
                db.session.commit()
                return redirect(url_for("user"))
            else:
                return error + ' <br> <a href="/user/">back</a>', 418

        if request.form.get("logout") is not None:
            session["username"] = ""
            return redirect(url_for("index"))

        elif request.form.get("delete") is not None:
            db.session.delete(user)
            db.session.commit()
            session["username"] = ""
            return redirect(url_for("index"))

        else:
            return "POST request with bad values.  Stop that!"
    else:
        if "username" not in session:
            session["username"] = ""
        return render_template("user.html", username=session["username"])


@app.route("/user/logout/", methods=["POST"])
def logout():
    session["username"] = ""


@app.route("/user/register/", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif UserModel.query.filter_by(username=username).first() is not None:
            error = f"User {username} is already registered."

        if error is None:
            new_user = UserModel(username, generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            session["username"] = username
            return redirect(url_for("index"))
        else:
            return error + ' <br> <a href="/user/register/">back</a>', 418
    else:
        if "username" not in session:
            session["username"] = ""
        return render_template(
            "login.html", mode="register", username=session["username"]
        )


@app.route("/user/login/", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        error = None

        user = UserModel.query.filter_by(username=username).first()

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user.password, password):
            error = "Incorrect password."

        if error is None:
            session["username"] = username
            return redirect(url_for("index"))
        else:
            return error + ' <br> <a href="/user/login">back</a>', 418
    else:
        if "username" not in session:
            session["username"] = ""
        return render_template("login.html", mode="login", username=session["username"])
