from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

category_association = db.Table('category_association',
    db.Column('project_id', db.Integer, db.ForeignKey('project.id'), primary_key = True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key = True),
    extend_existing=True
)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userName = db.Column(db.String(150), db.ForeignKey('user.uName'))
    categories = db.relationship('Category', secondary=category_association, backref='projects')
    course = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    description = db.Column(db.String(10000), nullable=False)
    githubLink = db.Column(db.String(100), nullable=False)
    contributors = db.Column(db.String(300)) #make it so users in this category have to be in Users database NOT DONE
    postStatus = db.Column(db.String(50), nullable=False, default = "unapproved") #unapproved, approved, archived, disapproved
    course_relation = db.relationship('Courses', back_populates='projects')

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(150), unique=True)
    uName = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    # profile_picture = db.Column(db.String(200), nullable=True) 
    isAdmin = db.Column(db.Boolean, nullable=False) #Would need to manually add users as admin either preBoot or through hidden page through root user
                                       #This would be done at project boot
    projects = db.relationship('Project')

class Courses(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    courseName = db.Column(db.String(50), nullable = False, unique=True)
    projects = db.relationship('Project', back_populates='course_relation')

class Category(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False, unique=True)

class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    project = db.relationship('Project', backref='bookmarked_by')
    user = db.relationship('User', backref='bookmarks')
