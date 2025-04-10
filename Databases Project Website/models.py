from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(20), nullable=False)
    categories = db.Column(db.String(100), nullable=False)
    course = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(10000), nullable=False)
    githubLink = db.Column(db.String(100),nullable=False)

#category = db.Table('category',
    #db.Column('id', db.Integer, db.ForeignKey('post.id')),
    #db.Column('category', db.String(100))
#)

#class Courses(db.Model):
    #id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    #course = db.Column(db.String(100), nullable = False)

#class Categories(db.Model):
    #id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    #category = db.Column(db.Sting(50), nullable = False)

