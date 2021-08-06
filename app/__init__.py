import os
from flask import Flask, render_template, request, session

from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.secret_key = (
    "iwaHjRoi3uOtJ64QONnL"
    "nEHkXfASet5RnDzpeL1n"
    "AUezFRYhoUYWvVkEvqBy"
    "GSbQ7M8jkA7I41mzo6ey"
    "PWT09pb8KZGszvMek0XB"
    "JBLWvO5D7WDzbWK5yHsi"
    "mXYwxouO9UDjyjsKBoUD"
    "a8Ttdn69XpOj5zzpvwtd"
    "LQha5BNXntVFBzJfYtBs"
    "KRX4vRKyzwmVyWGHVm21"
)

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


@app.route("/")
def index():
    username = ""
    if "username" in session:
        username = session["username"]
    return render_template("layout.html", username=username)


@app.route("/play/")
def modules():
    username = ""
    if "username" in session:
        username = session["username"]
    return render_template("modules.html")


@app.route("/user/")
def user():
    return (
        "TODO: make user page "
        '<form action="/logout/" method="post" target="_self"> '
        '<input type="submit" value="logout"> '
        "</form> "
        '<a href="/">home</a>'
    )


@app.route("/logout/", methods=["POST"])
def logout():
    session.pop("username")
    return 'logout successful. <a href="/">home</a>'


@app.route("/user/register/", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        error = None

        if not username:
            error = 'Username is required. <a href="/">home</a>'
        elif not password:
            error = 'Password is required. <a href="/">home</a>'
        elif UserModel.query.filter_by(username=username).first() is not None:
            error = f'User {username} is already registered. <a href="/">home</a>'

        if error is None:
            new_user = UserModel(username, generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            return f'User {username} created successfully. <a href="/">home</a>'
        else:
            return error, 418
    username = ""
    if "username" in session:
        username = session["username"]
    return render_template("login.html", mode="register", username=username)


@app.route("/user/login/", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        error = None

        user = UserModel.query.filter_by(username=username).first()

        if user is None:
            error = 'Incorrect username. <a href="/">home</a>'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password. <a href="/">home</a>'

        if error is None:
            session["username"] = username
            return 'Login successful. <a href="/">home</a>', 200
        else:
            return error, 418
        # TODO: Return a login page
    username = ""
    if "username" in session:
        username = session["username"]
    return render_template("login.html", mode="login", username=username)
