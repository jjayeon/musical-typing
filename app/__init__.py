import os
from flask import (
    Flask,
    render_template,
    request,
    session,
    redirect,
    url_for,
    make_response,
)

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
    return render_template("index.html", username=username)


@app.route("/play/")
def modules():
    username = ""
    if "username" in session:
        username = session["username"]
    return render_template("modules.html", username=username)


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
    return 'Logged out successfully. <a href="/">home</a>'


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
            return f'User {username} created successfully. <a href="/">home</a>'
        else:
            return error + ' <a href="/user/register/">back</a>', 418
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
            error = "Incorrect username."
        elif not check_password_hash(user.password, password):
            error = "Incorrect password."

        if error is None:
            return redirect('/', code=302)
        else:
            return error + ' <a href="/user/login">home</a>', 418
    username = ""
    if "username" in session:
        username = session["username"]
    return render_template("login.html", mode="login", username=username)
