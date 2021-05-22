import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import pytz

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
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")
    

@app.route("/changepassword", methods=["GET", "POST"])
@login_required
def changepassword():
    if request.method == "POST":
        if not request.form.get("newPassword"):
            return apology("MISSING PASSWORD", 400)
        db.execute("UPDATE users SET hash=? WHERE id=?", generate_password_hash(
            request.form.get("newPassword")), session["user_id"])
        return redirect("/")
    else:
        return render_template("changepassword.html")
    

@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    userInfo = db.execute("SELECT * FROM users WHERE id=?", session["user_id"])
    
    buy2_table_info = db.execute("SELECT * FROM buy2 WHERE username=?", userInfo[0]["username"])
    
    companies = []
    total_prices = []
    individual_prices = []
    total_current_stock_value = 0
    
    for i in range(0, len(buy2_table_info)):
        stock_info = lookup(buy2_table_info[i]["symbol"])
        
        companies.append(stock_info["name"])
        total_price = stock_info["price"]
        total_current_stock_value += total_price*buy2_table_info[i]["shares"]
        total_prices.append(usd(total_price*buy2_table_info[i]["shares"]))
        individual_prices.append(usd(stock_info["price"]))
        
    portfolio_value = float(userInfo[0]["cash"]) + total_current_stock_value
    
    return render_template("index.html", cash=usd(userInfo[0]["cash"]), info=buy2_table_info, companies=companies,
                           length=len(buy2_table_info), total_current_price=total_prices, individual_current_price=individual_prices, portfolio=usd(portfolio_value))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":
        
        if request.form.get("symbol") == None:
            return apology("MISSING SYMBOL", 400)
            
        if not request.form.get("shares"):
            return apology("MISSING SHARES", 400)
            
        if not request.form.get("shares").isdigit():
            return apology("INVALID AMOUNT", 400)

        if lookup(request.form.get("symbol")) == None:
            return apology("Invalid stock symbol", 400)

        userInfo = db.execute("SELECT * FROM users WHERE id=?", session["user_id"])

        stock = lookup(request.form.get("symbol"))

        price = stock["price"]
        symbol = stock["symbol"]
        numShares = int(request.form.get("shares"))

        if price*numShares > userInfo[0]["cash"]:
            return apology("Not enough money", 400)

        tz_NY = pytz.timezone('America/New_York')
        datetime_NY = datetime.now(tz_NY)

        db.execute("INSERT INTO buy (username, symbol, individualPrice, totalPrice, shares, datetime) VALUES(?, ?, ?, ?, ?, ?)",
                   userInfo[0]["username"], symbol, price, price*numShares, numShares, datetime_NY)

        same_stock_dif_time = db.execute("SELECT * FROM buy WHERE symbol=? AND username=?", symbol, userInfo[0]["username"])
        total_quantity_same_stock = 0
        total_price_same_stock = 0

        if len(same_stock_dif_time) != 1:
            for i in range(len(same_stock_dif_time)):
                total_price_same_stock += same_stock_dif_time[i]["totalPrice"]
                total_quantity_same_stock += same_stock_dif_time[i]["shares"]

            db.execute("UPDATE buy2 SET shares=?, total=? WHERE username=? AND symbol=?",
                       total_quantity_same_stock, total_price_same_stock, userInfo[0]["username"], symbol)
        else:
            db.execute("INSERT INTO buy2 (username, symbol, shares, total) VALUES(?, ?, ?, ?);",
                       userInfo[0]["username"], symbol, numShares, price*numShares)

        availableCash = userInfo[0]["cash"]

        db.execute("UPDATE users SET cash = ? WHERE id=?", availableCash - price*numShares, session["user_id"])

        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_info = db.execute("SELECT * FROM users WHERE id=?;", session["user_id"])
    history = db.execute("SELECT * FROM buy WHERE username=?;", user_info[0]["username"])
    
    return render_template("history.html", history=history, length=len(history))


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

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

        if (lookup(request.form.get("symbol")) == None):
            return apology("Enter a valid stock symbol", 400)
        else:
            stockInfo = lookup(request.form.get("symbol"))

        return render_template("quoted.html", info=stockInfo, price=usd(stockInfo["price"]))
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password") or not request.form.get("confirmation"):
            return apology("must provide password", 400)

        elif request.form.get("confirmation") != request.form.get("password"):
            return apology("Passwords Do Not Match", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct

        if len(rows) == 1:
            return apology("Username already exists. Please choose another one.", 400)

        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", request.form.get(
            "username"), generate_password_hash(request.form.get("password")))

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    
    if request.method == "POST":
        stock_symbol = request.form.get("symbol")
        if stock_symbol == "Default":
            return apology("MISSING STOCK", 400)
        if not request.form.get("shares"):
            return apology("MISSING SHARES", 400)
        
        num_shares = int(request.form.get("shares"))
        
        current_stock_info = lookup(stock_symbol)
        
        user_info = db.execute("SELECT * FROM users WHERE id=?;", session["user_id"])
        
        user_stock_info = db.execute("SELECT * FROM buy2 WHERE username=? AND symbol=?;", 
                                     user_info[0]["username"], stock_symbol)
            
        if user_stock_info[0]["shares"] < num_shares:
            return apology("NOT ENOUGH STOCKS", 400)
        
        db.execute("UPDATE users SET cash=? WHERE id=?;", 
                   current_stock_info["price"]*num_shares + user_info[0]["cash"], session["user_id"])
            
        db.execute("UPDATE buy2 SET shares=?, total=? WHERE username=? AND symbol=?;", 
                   user_stock_info[0]["shares"] - num_shares, (user_stock_info[0]
                                                               ["shares"] - num_shares)*current_stock_info["price"], 
                   user_info[0]["username"], stock_symbol)

        if user_stock_info[0]["shares"] - num_shares == 0:
            db.execute("DELETE FROM buy2 WHERE username=? AND symbol=? AND shares=?;", user_info[0]["username"], stock_symbol, 0)
        
        tz_NY = pytz.timezone('America/New_York')
        datetime_NY = datetime.now(tz_NY)
        
        db.execute("INSERT INTO buy (username, symbol, individualPrice, totalPrice, shares, datetime) VALUES(?, ?, ?, ?, ?, ?);", 
                   user_info[0]["username"], stock_symbol, current_stock_info["price"], current_stock_info["price"]*num_shares, num_shares*-1, datetime_NY)
        
        return redirect("/")

    else:
        user_info = db.execute("SELECT * FROM users WHERE id=?;", session["user_id"])
        stock = db.execute("SELECT * FROM buy2 WHERE username=?;", user_info[0]["username"])
        symbols = []
        for i in range(0, len(stock)):
            symbols.append(stock[i]["symbol"])
        return render_template("sell.html", symbols=symbols, length=len(stock))
    
    
def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
