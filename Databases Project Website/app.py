from flask import Flask, request, jsonify, render_template, flash, redirect, url_for, g
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Project, User, Courses, Category
from sqlalchemy import or_


app = Flask(__name__)

# Initialize LoginManager
login_manager = LoginManager()
login_manager.init_app(app)  # Attach it to the app

# Set the login_view to redirect users to the login page if they're not authenticated
login_manager.login_view = 'login'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.db'
app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)




with app.app_context():
    db.create_all()  # Creates the database tables
    if not Courses.query.first():   #populates the Courses table with values at app creation
        course_names = ["COMP 131", "COMP 373", "COMP 390", "COMP 490", "Personal Project"]
        for name in course_names:
            db.session.add(Courses(courseName=name))
        db.session.commit()

    if not User.query.first():   #populates the User table with admin user(s) at app creation
        db.session.add(User(email="root@gmail.com", uName="toor", password = generate_password_hash("rootoor", method='pbkdf2:sha256'), isAdmin=True))
        db.session.commit()

    if not Category.query.first(): #populates the Category table with values at app creation
        default_categories = ["Machine Learning", "Artificial Intelligence", "Web Development", "Game Development", "Natural Language Processing", "Data Science", "Other"]
        for category_name in default_categories:
            db.session.add(Category(name=category_name))
        db.session.commit() #is this redundant
        

# User loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def get_data_from_db():
    # Use SQLAlchemy to query the Project table
    projects = Project.query.all()  # Get all projects from the 'project' table
    courses = Courses.query.all()
    # Format the results as a list of dictionaries to pass to the template
    data = []
    for project in projects:
        project_data = {
            "id": project.id,
            "userName": project.userName,
            "categories": project.categories,
            "course": project.course,
            "description": project.description,
            "githubLink": project.githubLink,
            "contributors": project.contributors,
            "postStatus": project.postStatus
        }
        data.append(project_data)

    return data


def get_NOT_APPROVED_data_from_db():
    projects = Project.query.filter_by(postStatus="unapproved" or "disapproved" or "archived").all()
    data = []
    for project in projects:
        category_names = [cat.name for cat in project.categories]
        project_data = {
            "id": project.id,
            "userName": project.userName,
            "categories": category_names,
            "course": project.course_relation.courseName,
            "description": project.description,
            "githubLink": project.githubLink,
            "contributors": project.contributors,
            "postStatus": project.postStatus
        }
        data.append(project_data)
    return data


def get_APPROVED_data_from_db():
    # Use SQLAlchemy to query the Project table

    projects = Project.query.filter_by(postStatus = "approved").all()


    data = []
    for project in projects:
        category_names = [cat.name for cat in project.categories]
        project_data = {
            "id": project.id,
            "userName": project.userName,
            "categories": category_names,
            "course": project.course_relation.courseName,
            "description": project.description,
            "githubLink": project.githubLink,
            "contributors": project.contributors,
            "postStatus": project.postStatus
        }
        data.append(project_data)
    return data

@app.route('/admin')
@login_required
def admin():
    tempUser = User.query.filter_by(id=current_user.get_id()).first()
    if(tempUser.isAdmin == True):
        data = get_NOT_APPROVED_data_from_db()
        approvedData = get_APPROVED_data_from_db()
        return render_template('admin.html', data=data, approvedData = approvedData)
    else:
        return render_template('home.html')


@app.route('/approveProject', methods=['POST'])
def approve():
    data = request.json  

    if not isinstance(data, list):
        return jsonify(success=False, message="Invalid data format. Expecting a list of IDs."), 400

    try:
        Project.query.filter(Project.id.in_(data)).update(
            {Project.postStatus: "approved"},
            synchronize_session=False
        )
        db.session.commit()

        return jsonify(success=True, message="Project(s) approved successfully!")
    
    except Exception as e:
        db.session.rollback()
        return jsonify(success=False, message=str(e)), 500


@app.route('/un-approveProject', methods=['POST'])
def unApprove():
    data = request.json  

    if not isinstance(data, list):
        return jsonify(success=False, message="Invalid data format. Expecting a list of IDs."), 400

    try:
        Project.query.filter(Project.id.in_(data)).update(
            {Project.postStatus: "disapproved"},
            synchronize_session=False
        )
        db.session.commit()

        return jsonify(success=True, message="Project(s) un-approved successfully!")
    
    except Exception as e:
        db.session.rollback()
        return jsonify(success=False, message=str(e)), 500

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/submitProject')
@login_required
def submit():
    courses = Courses.query.all()
    categories = Category.query.all()

    # Sort categories, placing "Other" at the bottom
    categories_sorted = sorted([cat for cat in categories if cat.name != "Other"], key=lambda x: x.name)
    other_category = next((cat for cat in categories if cat.name == "Other"), None)
    if other_category:
        categories_sorted.append(other_category)  # Append "Other" at the end

    # Sort courses, placing "Personal Project" at the bottom
    courses_sorted = sorted([course for course in courses if course.courseName != "Personal Project"], key=lambda x: x.courseName)
    personal_project_course = next((course for course in courses if course.courseName == "Personal Project"), None)
    if personal_project_course:
        courses_sorted.append(personal_project_course)  # Append "Personal Project" at the end

    return render_template('submit.html', courses=courses_sorted, categories=categories_sorted)


@app.route('/grabProject', methods=['GET'])
def getProject():
    return jsonify()


@app.route('/putProject', methods=['POST'])
def putProject():
    userInfo = ''

    if current_user.is_authenticated: 
        g.user = current_user.get_id()
        tempUser = User.query.filter_by(id=current_user.get_id()).first()
        userInfo = tempUser.uName

    data = request.json

    projectUser = userInfo
    projectCategories = data.get('projectCategories', [])
    categories = Category.query.filter(Category.id.in_(projectCategories)).all()  # Filter categories by IDs
    projectCourse = int(data.get('projectCourse'))  # Convert to integer for ID
    projectDescription = data.get('projectDescription')
    projectLink = data.get('projectLink')
    projectContributors = data.get('projectContributors')
    projectApproval = "unapproved"

    if projectContributors == '':
        projectContributors = "N/A"

    if not Courses.query.get(projectCourse):
        return jsonify(success=False, message="Invalid course ID"), 400

    newProject = Project(
        userName=projectUser,
        categories=categories,  # Assign selected categories
        description=projectDescription,
        course=projectCourse,
        githubLink=projectLink,
        contributors=projectContributors,
        psotStatus=projectApproval
    )

    db.session.add(newProject)
    db.session.commit()

    return jsonify(success=True, message="Project added successfully")


@app.route('/addCourse', methods=['POST'])
@login_required
def add_course():
    # Ensure only admins can add courses
    if not current_user.isAdmin:
        return jsonify(success=False, message="Permission denied"), 403
    
    data = request.json
    course_name = data.get('courseName')

    if not course_name:
        return jsonify(success=False, message="Course name is required"), 400

    new_course = Courses(courseName=course_name)
    db.session.add(new_course)
    db.session.commit()

    return jsonify(success=True, message="Course added successfully!")

@app.route('/addCategory', methods=['POST'])
@login_required
def add_category():
    # Ensure only admins can add categories
    if not current_user.isAdmin:
        return jsonify(success=False, message="Permission denied"), 403

    data = request.json
    category_name = data.get('categoryName')

    if not category_name:
        return jsonify(success=False, message="Category name is required"), 400

    new_category = Category(name=category_name)
    db.session.add(new_category)
    db.session.commit()

    return jsonify(success=True, message="Category added successfully!")


@app.route('/exploreProjects')
def explore():
    categories = Category.query.all()
    return render_template('explore.html', categories=categories)

@app.route('/exploreX', methods=['POST'])
def exploreX():
    selected_categories = request.form.getlist('categories')

    if selected_categories:
        #filtered_projects = Project.query.filter(Project.categories.in_(selected_categories)).all()
        filtered_projects = Project.query.join(Project.categories).filter(Category.name.in_(selected_categories)).all()
        #filtered_projects = Project.query.filter(or_(*filters)).all()
    else:
        filtered_projects = Project.query.all()

    return render_template('list.html',
                           data=filtered_projects,
                           selected_categories=selected_categories)

@app.route('/projectList')
def allProjects():
    return render_template('list.html', data = Project.query.all())

@app.route('/list')
def projects():
    data = get_data_from_db()  # Call the function to get data
    print (data)
    return render_template('list.html', data=data) 




@app.route('/test', methods=['GET'])
def test():
    allProjects = []

    projectValues = Project.query.all()


    for projects in projectValues:
        project_data = {
            "id": projects.id,
            "username": projects.userName,
            "description": projects.description,
            "categories": [cat.id for cat in projects.categories], #does it make more sense to see ids or names?
            "courseId": projects.course,
            "githubLink": projects.githubLink,
            "contributors": projects.contributors,
            "postStatus": projects.postStatus
        }


        allProjects.append(project_data)

    return jsonify(allProjects)

@app.route('/testUsers', methods=['GET'])
def testUsers():
    allUsers = []

    userValues = User.query.all()

    for users in userValues:
        user_data = {
            "id": users.id,
            "userName": users.uName,
            "email": users.email,
            "password": users.password,
            "isAdmin": users.isAdmin

        }

        allUsers.append(user_data)

    return jsonify(allUsers)


@app.route('/testCourses', methods=['GET'])
def testCourses():
    allCourses = []

    courseValues = Courses.query.all()

    for course in courseValues:
        course_data = {
            "id": course.id,
            "courseName": course.courseName
        }

        allCourses.append(course_data)

    return jsonify(allCourses)


@app.route('/testCat', methods=['GET'])
def testCat():
    allCats = []

    catValues = Category.query.all()

    for cats in catValues:
        cat_data = {
            "id": cats.id,
            "name": cats.name

        }

        allCats.append(cat_data)

    return jsonify(allCats)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))  # Redirect to homepage if already logged in

    message = None
    message_type = None  # to track whether it's a success or error message
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            message = 'Logged in successfully!'
            message_type = 'success'
            login_user(user, remember=True)
            return redirect(url_for('index'))
        elif user is None:
            message = 'Email does not exist.'
            message_type = 'error'
        else:
            message = 'Incorrect password, try again.'
            message_type = 'error'
        

    return render_template("login.html", user=current_user, message=message, message_type=message_type)


@app.route('/logout')
@login_required
def logout():
    logout_user()  # Logs the user out
    return redirect(url_for('index'))  # Redirect to the home page



@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('index'))  # Redirect to homepage if already logged in

    message = None
    message_type = None  # to track whether it's a success or error message
    
    if request.method == 'POST':
        email = request.form.get('email')
        uName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # Validation
        if User.query.filter_by(email=email).first():
            message = 'Email already in use.'
            message_type = 'error'
        elif len(email) < 4:
            message = 'Email must be greater than 3 characters.'
            message_type = 'error'
        elif len(uName) < 2:
            message = 'First name must be greater than 1 character.'
            message_type = 'error'
        elif password1 != password2:
            message = 'Passwords don\'t match.'
            message_type = 'error'
        elif len(password1) < 7:
            message = 'Password must be at least 7 characters.'
            message_type = 'error'
        else:
            # if(email == 'root@gmail.com'):
            #     isAdminValue = True
            # else:
            isAdminValue = False

            new_user = User(email=email, uName=uName, password=generate_password_hash(password1, method='pbkdf2:sha256'), isAdmin= isAdminValue)
            db.session.add(new_user)
            db.session.commit()
            message = 'Account created successfully!'
            message_type = 'success'
            login_user(new_user, remember=True)
            
            flash('Created account sucessfully!', category='success') #DOESN"T SHOW TO USER FOR SOME REASON???

            return redirect(url_for('index'))  # Redirect to home page

    return render_template("sign-up.html", user=current_user, message=message, message_type=message_type)



if __name__ == '__main__':
    app.run(debug=True)
