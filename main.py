import random
from flask import Flask, render_template, request, make_response, redirect, url_for, flash
from models import User, db

app = Flask(__name__)
app.secret_key = ("super-secret-key")

db.create_all()

@app.route("/", methods=["GET"])
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

    secret_number = random.randint(1, 30)

    user = db.query(User).filter_by(email=email).first()

    if not user:
        user = User(name=name, email=email, secret_number=secret_number)
        db.add(user)
        db.commit()

    response = make_response(redirect(url_for('index')))
    response.set_cookie("email", email)

    return response


@app.route("/result", methods=["POST"])
def game():
    guess = int(request.form.get("guess"))
    email_address = request.cookies.get("email")
    user = db.query(User).filter_by(email=email_address).first()

    if guess == user.secret_number:
        message = f"Nice! You guessed the right number, secret number was: {user.secret_number}"
        flash(message)
        new_secret = random.randint(1, 30)
        user.secret_number = new_secret
        db.add(user)
        db.commit()

    elif guess > user.secret_number:
        message = f"Your guessing number: {guess} is too high!"
        flash(message)

    elif guess < user.secret_number:
        message = f"Your guessing number: {guess} is too low!"
        flash(message)

    return render_template("result.html", message=message)
