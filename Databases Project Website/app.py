from flask import Flask, request, jsonify, render_template, Blueprint  
from models import db, Project

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()  # Creates the database tables



# Sets home.html to / (root/start page)
@app.route('/')
def index():
    return render_template('home.html')


@app.route('/submitProject')
def submit():
    return render_template('submit.html')


@app.route('/exploreProjects')
def explore():
    return render_template('explore.html')

@app.route('/grabProject', methods=['GET'])  #NOT SETUP YET
def getTutorial():
    return jsonify()

@app.route('/putProject',methods=['POST'])
def putTutorial():
    return jsonify(success=True, message="Tutorial added successfully")


if __name__ == '__main__':
    app.run(debug=True)