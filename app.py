import itertools #This is a module in the standard library whicb can iterate to allow for efficiency
from flask import Flask, render_template, request, redirect, url_for #Flask allows me to create a backend for the website
import hashlib #This is a module which allows me to hash passwords - even I can't see them!
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
app = Flask(__name__) 
limiter = Limiter(get_remote_address, app=app)

@app.route('/', methods=["GET", "POST"])
@limiter.limit("10 per minute")
def index():
    if request.method == "POST":
        logged_in = False
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        number_of_the_line = None
        if username:
            with open("database.txt", "r") as f:
                    unames = [line.strip() for line in f.readlines()]
                    for the_line in unames:
                        if the_line.startswith(username + ","):
                            number_of_the_line = the_line
                            break
        if number_of_the_line is not None and password:
            password_on_file = number_of_the_line.split(",")[1].strip()
            if password_on_file == hashlib.sha256(password.encode()).hexdigest():
                logged_in = True
                return redirect(url_for('thief'))
        return render_template('index.html', logged_in=logged_in, username=username, password=password)
    return render_template('index.html', logged_in=False, username="", password="") 

@app.route("/thief", methods=["POST", "GET"])
@limiter.limit("10 per minute")
def thief():
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
            print("Ooops, it would seem like you haven't inputted a number, please try again!")
    return render_template("thief.html", ans="", num1="", num2="", num3="", num4="")

@app.route("/register", methods=["POST", "GET"])
@limiter.limit("10 per minute")
def register():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if username and password:
            with open("database.txt", "r") as f:
                    for line in f:
                        if line.strip().split(",")[0] == username:
                            exists = True
                            break
            if exists:
                message = "Username already exists. Please choose a different username."
                return render_template('register.html', message=message, username=username, password=password)
            with open("database.txt", "a") as f:
                f.write(f"{username},{hashlib.sha256(password.encode()).hexdigest()}\n")
            return redirect(url_for('index'))
        return render_template('register.html', username=username, password=password, message="Please fill in both fields.")
    return render_template('register.html', username="", password="", message="")

@app.route("/police", methods=["POST", "GET"])
@limiter.limit("10 per minute")
def police():
    criminals = []
    with open("database.txt", "r") as f:
            for line in f:
                username = line.strip().split(",")[0]
                criminals.append(username)
    return render_template('police.html', criminals=criminals)            