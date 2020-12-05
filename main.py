import random
from datetime import date
from flask import Flask, render_template, request, make_response, redirect, url_for, flash
from models import User, db

app = Flask(__name__)
app.secret_key = ("super-secret-key")

db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    email_address = request.cookies.get("email")
    if email_address:
        user = db.query(User).filter_by(email=email_address).first()
    else:
        user = None
    return render_template("index.html", user=user)


@app.route("/login", methods=["POST"])
def login():
    name = request.form.get("name")
    email = request.form.get("email")
    today = date.today()
    secret_number = random.randint(1, 30)
    attempts = 0
    best_score = 999
    user = db.query(User).filter_by(email=email).first()

    if not user:
        user = User(name=name, email=email, secret_number=secret_number, date=today, attempts=attempts, best_score=best_score)
        db.add(user)
        db.commit()

    response = make_response(redirect(url_for('un')))
    response.set_cookie("email", email)
    response.set_cookie("name", name)
    response.set_cookie("date", today.strftime("%d/%m/%Y"))
    return response


@app.route("/result", methods=["POST"])
def game():
        email_address = request.cookies.get("email")
        user = db.query(User).filter_by(email=email_address).first()
        guess = int(request.form.get("guess"))
        attempts = 0
        attempts += 1
        user.attempts = user.attempts + attempts
        db.add(user)
        db.commit()

        if guess == user.secret_number:
            message = f"Nice! You guessed the right number, secret number was: {user.secret_number}. Number of attempts to guess: {user.attempts}"
            flash(message)
            new_secret = random.randint(1, 30)
            user.secret_number = new_secret
            db.add(user)
            db.commit()
            if user.attempts < user.best_score:
                user.best_score = user.attempts
                user.attempts = 0
                db.add(user)
                db.commit()
        elif guess > user.secret_number:
            message = f"Your guessing number: {guess} is too high! Current numbers of attempts: {user.attempts}"
            flash(message)
        elif guess < user.secret_number:
            message = f"Your guessing number: {guess} is too low! Current numbers of attempts: {user.attempts}"
            flash(message)
            return render_template("result.html", message=message)
        return render_template("result.html", message=message)

@app.route("/user", methods=["GET", "POST"])
def un():
    email = request.cookies.get("email")
    user = db.query(User).filter_by(email=email).first()
    username = user.name
    input_name = request.form.get("name")
    if username == input_name:
        response = make_response(redirect(url_for('index')))
        return response
    else:
        message = f"Wrong username, try again!"
        flash(message)
    return render_template("user.html", message=message)