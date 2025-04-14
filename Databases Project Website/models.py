from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userName = db.Column(db.String(150), db.ForeignKey('user.uName'))
    categories = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(10000), nullable=False)
    githubLink = db.Column(db.String(100), nullable=False)
    contributors = db.Column(db.String(300)) #make it so users in this category have to be in Users database NOT DONE
    isApproved = db.Column(db.Boolean, nullable=False)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(150), unique=True)
    uName = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    isAdmin = db.Column(db.Boolean, nullable=False) #Would need to manually add users as admin either preBoot or through hidden page through root user
                                       #This would be done at project boot
    projects = db.relationship('Project')