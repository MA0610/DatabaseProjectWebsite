from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

category_association = db.Table('category_association',
    db.Column('project_id', db.Integer, db.ForeignKey('project.id'), primary_key = True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key = True),
    extend_existing=True
)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(20), nullable=False)
    categories = db.Column(db.String(100), nullable=False)
    course = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    description = db.Column(db.String(10000), nullable=False)
    githubLink = db.Column(db.String(100),nullable=False)

    course_relation = db.relationship('Courses', back_populates='projects')

class Courses(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    courseName = db.Column(db.String(50), nullable = False)
    projects = db.relationship('Project', back_populates='course_relation')

class Category(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    category = db.Column(db.String(50), nullable = False, unique=True)
