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

#sample lsit page with all projects of a certain category listed
@app.route('/exploreX')
def exploreX():
    return render_template('list.html')

@app.route('/grabProject', methods=['GET'])  #NOT SETUP YET
def getTutorial():
    return jsonify()

@app.route('/putProject',methods=['POST'])
def putProject():
    data = request.json

    projectUser = data.get('projectAuthor')
    projectCategories = data.get('projectCategories')
    projectDescription = data.get('projectDescription')
    projectLink = data.get('projectLink')
  
    newProject = Project(
        userName = projectUser,
        categories = projectCategories,
        description = projectDescription,
        githubLink = projectLink
    )

    db.session.add(newProject)
    db.session.commit()

    return jsonify(success=True, message="Project added successfully")


@app.route('/test', methods=['GET'])
def test():
    allProjects = []

    projectValues = Project.query.all()

    for projects in projectValues:
        project_data = {
            "id": projects.id,
            "username": projects.userName,
            "description": projects.description,
            "categories": projects.categories,
            "githubLink": projects.githubLink
        }
    
        allProjects.append(project_data)
        print(project_data)
    
    

    return jsonify(allProjects)



if __name__ == '__main__':
    app.run(debug=True)
