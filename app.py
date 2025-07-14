import sqlite3
import os
import itertools #This is a module in the standard library whicb can iterate to allow for efficiency
from flask import Flask, render_template, request, redirect, url_for, session, render_template_string #Flask allows me to create a backend for the website
import hashlib #This is a module which allows me to hash passwords - even I can't see them!
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
app = Flask(__name__) 
limiter = Limiter(get_remote_address, app=app)
load_dotenv()
app.secret_key = os.environ.get('FLASK_SECRET_KEY')

def get_db():
    conn = sqlite3.connect("main.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route('/', methods=["GET", "POST"])
@limiter.limit("20 per minute")
def index():
    cookies_accepted = request.cookies.get('cookies_accepted')
    message = None
    if request.args.get("redirect") == "True":
        message = "To view that page please log in."
    if request.args.get("unameredirect") == "True":
        message = "Your account dosen't have the neccessary permissions to access that page."
    if request.method == "POST":
        logged_in = False
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
        row = c.fetchone()
        conn.close()
        if row and password and row["password_hash"] == hashlib.sha256(password.encode()).hexdigest() and cookies_accepted == "true":
            logged_in = True
            session["logged_in"] = True
            session["username"] = username
            return redirect(url_for('thief'))
        elif username == "police" and password == "fbi":
            session["logged_in"] = True
            session["username"] = username
            return redirect(url_for("police"))
        return render_template('index.html', logged_in=logged_in, username=username, password=password)
    return render_template('index.html', logged_in=False, username="", password="", redirect_message=message) 

@app.route("/thief", methods=["POST", "GET"])
@limiter.limit("10 per minute")
def thief():
    if not session.get("logged_in"):
        return redirect(url_for("index", redirect=True))
    if request.method == "POST":
        try: 
            #taking inputs from the user
            num1 = str(int(request.form.get("num1", "")))
            num2 = str(int(request.form.get("num2", "")))
            num3 = str(int(request.form.get("num3", "")))
            num4 = str(int(request.form.get("num4", "")))
            nums = [num1, num2, num3, num4] 
            rearrangement = [" ".join(x) for x in itertools.permutations(nums, 4)] 
            ans = []
            for y in rearrangement:
                ans.append(y)
            ans = list(set(ans)) # This ensure that I can remove duplicated ones
            print(ans)
            return render_template('thief.html', ans=ans, num1=num1, num2=num2, num3=num3, num4=num4)
        except ValueError:
            pass #Nothing needed here
    return render_template("thief.html", ans="", num1="", num2="", num3="", num4="")

@app.route("/register", methods=["POST", "GET"])
@limiter.limit("10 per minute")
def register():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if username and password:
            conn = get_db()
            c = conn.cursor()
            c.execute("SELECT 1 FROM users WHERE username = ?", (username,))
            exists = c.fetchone()
            if exists:
                conn.close()
                message = "Username already exists. Please choose a different username."
                return render_template('register.html', message=message, username=username, password=password)
            c.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                      (username, hashlib.sha256(password.encode()).hexdigest()))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        return render_template('register.html', username=username, password=password, message="Please fill in both fields.")
    return render_template('register.html', username="", password="", message="")

@app.route("/police", methods=["POST", "GET"])
@limiter.limit("10 per minute")
def police():
    if not session.get("logged_in"):
        return redirect(url_for("index", redirect=True))
    elif session.get("username") != "police":
        return redirect(url_for("index", unameredirect=True))
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT username FROM users")
    criminals = [row["username"] for row in c.fetchall()]
    conn.close()
    return render_template('police.html', criminals=criminals)          