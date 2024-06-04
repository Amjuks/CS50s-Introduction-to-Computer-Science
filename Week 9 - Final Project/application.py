# imports class to run SQL queries
from cs50 import SQL

# imports flask
from flask import Flask, redirect, render_template, request, session
from flask_session import Session

# imports templfile to make a temporary directory
from tempfile import mkdtemp

# imports werkzeug for security and catching errors and exceptions
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

# imports my own module
from pokeBackend import login_required, apology, lookup, fav, colorCode, TypeSplit, searchPoke, log

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///pokedex.db")

@app.route("/", methods = ["GET", "POST"])
@login_required
def index():
    return searchPoke([], "index.html", db.execute("SELECT id, name, type, url FROM dex"))


@app.route("/search", methods = ["GET", "POST"])
@login_required
def search():
    return searchPoke(["Search", "/search", "Search by name or global ID!"], "search")


@app.route("/type", methods = ["GET", "POST"])
@login_required
def searchType():
    return searchPoke(["Type", "/type", "Search by Type or Type ID!"], "type")


@app.route("/moves", methods = ["GET", "POST"])
@login_required
def searchMoves():
    return searchPoke(["Moves", "/moves", "Search by moves!"], "move")


@app.route("/ability", methods = ["GET", "POST"])
@login_required
def searchAbility():
    return searchPoke(["Ability", "/ability", "Search by ability!"], "ability")


@app.route("/favourite", methods = ["GET", "POST"])
@login_required
def favourite():
    return searchPoke([], "favourites.html", db.execute("SELECT id, name, type, url FROM dex WHERE id IN (:fav)", fav = fav("list")))


@app.route("/pokemon")
@login_required
def pokemon():
    poke = db.execute("SELECT * FROM dex WHERE id = :poke_id", poke_id = request.args.get('id'))[0]
    log(f"{ session['name'] } clicked { poke['name']}")
    return render_template("pokemon.html", poke = poke, color = colorCode)


# register route
@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":

        # intializing variables to the values
        username = request.form.get("username")
        password = request.form.get("password")

        # returns apology if username exists
        if len(db.execute("SELECT * FROM users WHERE name = :username", username = username)) == 1:
            return apology("Username Exists", "Register")

        # generates a hash for the password
        key = generate_password_hash(password)

        # inserts user credentials
        db.execute("INSERT INTO users (name, hash) VALUES(:username, :key)", username = username, key = key)

        # user gets logged in
        session["user_id"] = db.execute("SELECT id FROM users WHERE name = :username", username = username)[0]["id"]
        session['offset'] = 0
        session['page'] = []

        # logs information about who had registered
        log(f"{session['user_id']} registered")
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/login", methods = ["GET", "POST"])
def login():
    """Log user in"""

    title = "Login"
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", title)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", title)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE name = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", title)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session['name'] = rows[0]['name']
        log(f"User {session['user_id'], session['name']} logged in")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()
    log(f"{session['user_id'] if 'user_id' in session else 'Server restarted, unknown user'} logged out")

    # Redirect user to login form
    return redirect("/login")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)