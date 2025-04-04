from flask import Flask, request, jsonify, render_template, Blueprint  
from models import db, Project

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()  # Creates the database tables

def get_data_from_db():
    # Use SQLAlchemy to query the Project table
    projects = Project.query.all()  # Get all projects from the 'project' table

    # Format the results as a list of dictionaries to pass to the template
    data = []
    for project in projects:
        project_data = {
            "id": project.id,
            "userName": project.userName,
            "categories": project.categories,
            "description": project.description,
            "githubLink": project.githubLink
        }
        data.append(project_data)

    return data

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

#sample lsit page with all projects of selected categories listed
#@app.route('/exploreX')
#def exploreX():
#    return render_template('list.html')
@app.route('/exploreX', methods=['POST'])
def exploreX():
    selected_categories = request.form.getlist('categories')

    if selected_categories:
        filtered_projects = Project.query.filter(Project.categories.in_(selected_categories)).all()
    else:
        filtered_projects = Project.query.all()

    return render_template('list.html',
                           data=filtered_projects,
                           selected_categories=selected_categories)


@app.route('/grabProject', methods=['GET'])  #NOT SETUP YET
def getTutorial():
    return jsonify()

@app.route('/list')
def projects():
    data = get_data_from_db()  # Call the function to get data
    print (data)
    return render_template('list.html', data=data)

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
