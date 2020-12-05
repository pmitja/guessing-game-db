import os, datetime
from sqla_wrapper import SQLAlchemy

db = SQLAlchemy(os.getenv("DATABASE_URL", "sqlite:///my_guessing_game_base.sqlite"))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    secret_number = db.Column(db.Integer, unique=False)
    date = db.Column(db.DateTime)
    attempts = db.Column(db.Integer)
    best_score = db.Column(db.Integer)