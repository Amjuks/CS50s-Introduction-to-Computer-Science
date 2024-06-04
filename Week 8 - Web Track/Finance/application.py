import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

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


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
# if not os.environ.get("API_KEY"):
#    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    stocks = db.execute("SELECT stock, SUM(shares) AS shares FROM stocks WHERE user_id = :user_id  GROUP BY stock HAVING SUM(shares) > 0",
    user_id=session['user_id'])
    balance = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id = session['user_id'])[0]['cash']

    grand_total = 0.00

    for i in range(len(stocks)):
        stock = lookup(stocks[i]['stock'])
        stocks[i]['name'] = stock['name']
        stocks[i]['cur_price'] = stock['price']
        stocks[i]['cur_total'] = stock['price'] * stocks[i]['shares']
        grand_total += stocks[i]['cur_total']

    grand_total += balance

    return render_template("index.html", stocks = stocks, total = grand_total, balance = balance)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":

        stock = request.form.get("symbol").upper()
        shares = int(request.form.get("shares"))

        if not stock:
            return apology("Must provide symbol")

        if not shares or shares < 0:
            return apology("Number of shares invalid")

        rows = lookup(stock)

        if not rows:
            return apology("Invalid symbol")

        total = shares * rows['price']
        balance = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id = session['user_id'])[0]['cash']

        if not total <= balance:
            return apology("You cannot afford the share")

        db.execute("UPDATE users SET cash = :balance WHERE id = :user_id", balance = (balance - total), user_id = session['user_id'])
        db.execute("INSERT INTO stocks (user_id, stock, shares, cur_price, total) VALUES (:user_id, :stock, :shares, :cur_price, :total)",
        user_id=session['user_id'], stock = stock, shares = shares, cur_price = rows['price'], total = total)

        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    rows = db.execute("SELECT stock, shares, cur_price, timestamp FROM stocks WHERE user_id = :user_id ORDER BY timestamp DESC", user_id = session['user_id'])
    return render_template("history.html", rows = rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

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

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":
        rows = lookup(request.form.get("symbol"))

        if not rows:
            return apology("Invalid Symbol")

        info = (f"A share of {rows['name']} ({rows['symbol']}) costs ${rows['price']}.")
        return render_template("quoted.html", info = info)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return apology("Username Required")

        if not password:
            return apology("Password Required")

        if not request.form.get("confirmation"):
            return apology("Required Confirmation")

        if len(db.execute("SELECT * FROM users WHERE username = :username", username = username)) == 1:
            return apology("Username Exists")

        if password != request.form.get("confirmation"):
            return apology("Confirmation Error")

        key = generate_password_hash(request.form.get("password"))

        db.execute("INSERT INTO users (username, hash) VALUES(:username, :key)", username = username, key = key)

        session["user_id"] = db.execute("SELECT id FROM users WHERE username = :username", username = username)[0]["id"]
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session['user_id']

    if request.method == "POST":

        shares = int(db.execute("SELECT SUM(shares) FROM stocks WHERE user_id = :user_id", user_id = user_id)[0]['SUM(shares)'])
        share = int(request.form.get("shares"))
        info = lookup(request.form.get("symbol"))
        total = (info['price'] * share)

        if share > shares:
            return apology("Too many shares")

        db.execute("INSERT INTO stocks (user_id, stock, shares, cur_price, total) VALUES (:user_id, :stock, :shares, :cur_price, :total)",
        user_id=user_id, stock = request.form.get("symbol"), shares = (share * -1), cur_price = info['price'], total = total)

        balance = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id = user_id)[0]['cash']
        db.execute("UPDATE users SET cash = :balance WHERE id = :user_id", balance = balance + total, user_id = user_id)

        return redirect("/")

    else:
        symbols_list = db.execute("SELECT stock FROM stocks WHERE user_id = :user_id  GROUP BY stock HAVING SUM(shares) > 0",
        user_id=session['user_id'])

        symbols = []

        for symbol in symbols_list:
            symbols.append(symbol['stock'])

        return render_template("sell.html", symbols = symbols)

@app.route("/changepassword", methods = ["GET", "POST"])
def changePassword():
    """Change user password"""
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        elif not request.form.get("newPassword"):
            return apology("Enter New Password", 403)

        elif not request.form.get("newPassword-confirmation"):
            return apology("Enter password confirmation", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        if request.form.get("newPassword") != request.form.get("newPassword-confirmation"):
            return apology("Password Confirmation Error")

        password = generate_password_hash(request.form.get("newPassword"))

        user_id = db.execute("UPDATE users SET hash = :password WHERE username = :username", password = password, username = request.form.get("username"))

        session['user_id'] = user_id
        return redirect("/")

    else:
        return render_template("password.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)