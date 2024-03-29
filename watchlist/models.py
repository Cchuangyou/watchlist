from flask_login import UserMixin
from watchlist import db
from werkzeug.security import generate_password_hash, check_password_hash

# create database model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Movie(db.Model):  # list name: movie
    id = db.Column(db.Integer, primary_key=True)  # subject
    title = db.Column(db.String(60))  # movie title
    year = db.Column(db.String(4))  # movie years