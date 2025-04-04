from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(20), nullable=False)
    categories = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(10000), nullable=False)
    githubLink = db.Column(db.String(100),nullable=False)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(150), unique=True)
    first_name = db.Column(db.String(150))
    password = db.Column(db.String(150))
    # user = db.relationship('Project')