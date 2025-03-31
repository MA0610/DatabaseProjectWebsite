from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(20), nullable=False)
    categories = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(10000), nullable=False)
    githubLink = db.Column(db.String(100),nullable=False)

