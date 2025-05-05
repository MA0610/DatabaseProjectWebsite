from flask import Flask, request, jsonify, render_template, flash, redirect, url_for, g#, flash
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Project, User, Courses, Category, Bookmark
from sqlalchemy import or_

# import os
# from werkzeug.utils import secure_filename

# # Define the path for uploading
# UPLOAD_FOLDER = os.path.join('static', 'uploads')
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)

# Initialize LoginManager
login_manager = LoginManager()
login_manager.init_app(app)  # Attach it to the app

# Set the login_view to redirect users to the login page if they're not authenticated
login_manager.login_view = 'login'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB limit
# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# # File upload settings
# UPLOAD_FOLDER = 'static/uploads/'
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # max file size: 16MB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.db'
app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)




with app.app_context():
    db.create_all()  # Creates the database tables


     if not Project.query.first():   
        projects_info = [Project(userName="Matthew Arboleda",catgories="Web Development",course="COMP 367",
                        description="This project is a scheduling website meant to help professors at Occidental communicate when each class should be to avoid having important classes at the same time before sending the schedule to the registrar's office. This website uses Python, SQLAlchemy, and Flask", 
                        githubLink="https://github.com/MA0610/SchedulingWebsite",contributors="Diego Santiago, Jose Bustamente Ortiz, Marvin Romero", postStatus="unapproved"),Project(userName="Matthew Arboleda",catgories="Web Development",course="Personal Project",
                        description="This is an e-plant shopping website using REACT, this was made for IBM's developing front-end apps using REACT course.", 
                        githubLink="https://github.com/MA0610/e-plantShopping",contributors="", postStatus="unapproved")]
        for name in projects_info:
            db.session.add(projects_info)
        db.session.commit()
    
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
    #projects = Project.query.filter_by(postStatus='unapproved' or 'disapproved' or 'archived').all()
    projects = Project.query.filter(Project.postStatus.in_(['unapproved', 'disapproved', 'archived'])).all()
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

    projects = Project.query.filter_by(postStatus='approved').all()


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
        postStatus=projectApproval
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

    bookmarked_ids = []
    if current_user.is_authenticated:
        bookmarked_ids = [b.project_id for b in current_user.bookmarks]

    return render_template('explore.html',
                           data=filtered_projects,
                           selected_categories=selected_categories,
                           categories=Category.query.all(),
                           bookmarked_project_ids=bookmarked_ids)

@app.route('/projectList')
def allProjects():
    return render_template('list.html', data = Project.query.all())

@app.route('/list')
def projects():
    data = get_data_from_db()  # Call the function to get data
    print (data)
    return render_template('list.html', data=data) 

# @app.route('/upload_profile_pic', methods=['POST'])
# @login_required
# def upload_profile_pic():
#     if 'profile_pic' not in request.files:
#         flash('No file part')
#         return redirect(request.url)

#     file = request.files['profile_pic']
#     if file.filename == '':
#         flash('No selected file')
#         return redirect(request.url)

#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(file_path)

#         # Save file path to user's database entry
#         user = User.query.get(current_user.id)
#         user.profile_picture = filename
#         db.session.commit()

#         flash('Profile picture updated!')
#         return redirect(url_for('profile'))

#     flash('Invalid file type')
#     return redirect(request.url)

@app.route('/my-bookmarks')
@login_required
def my_bookmarks():
    bookmarks = Bookmark.query.filter_by(user_id=current_user.id).all()
    projects = [b.project for b in bookmarks]
    return render_template('bookmarks.html', projects=projects)

@app.route('/bookmark/<int:project_id>', methods=['POST'])
@login_required
def bookmark_project(project_id):
    existing = Bookmark.query.filter_by(user_id=current_user.id, project_id=project_id).first()
    if existing:
        return jsonify(success=False, message="Already bookmarked.")
    new_bookmark = Bookmark(user_id=current_user.id, project_id=project_id)
    db.session.add(new_bookmark)
    db.session.commit()
    return jsonify(success=True, message="Bookmarked successfully!")
    
@app.route('/unbookmark/<int:project_id>', methods=['POST'])
@login_required
def unbookmark_project(project_id):
    bookmark = Bookmark.query.filter_by(user_id=current_user.id, project_id=project_id).first()
    if bookmark:
        db.session.delete(bookmark)
        db.session.commit()
        return jsonify(success=True, message="Removed bookmark.")
    return jsonify(success=False, message="Bookmark not found.")
    
@app.route('/toggle-bookmark/<int:project_id>', methods=['POST'])
@login_required
def toggle_bookmark(project_id):
    bookmark = Bookmark.query.filter_by(user_id=current_user.id, project_id=project_id).first()
    if bookmark:
        db.session.delete(bookmark)
        db.session.commit()
        return jsonify(success=True, action='removed')
    else:
        new_bookmark = Bookmark(user_id=current_user.id, project_id=project_id)
        db.session.add(new_bookmark)
        db.session.commit()
        return jsonify(success=True, action='added')

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    message = None
    message_type = None
    
    if request.method == 'POST':
        new_username = request.form.get('username')
        new_email = request.form.get('email')
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        user = User.query.get(current_user.id)

        if new_username:
            user.uName = new_username

        if new_email:
            if User.query.filter_by(email=new_email).first() and new_email != current_user.email:
                message = 'Email already in use.'
                message_type = 'error'
            else:
                user.email = new_email

        # Handle password change
        if current_password and new_password and confirm_password:
            if not check_password_hash(user.password, current_password):
                message = 'Current password is incorrect.'
                message_type = 'error'
            elif new_password != confirm_password:
                message = 'New passwords do not match.'
                message_type = 'error'
            elif len(new_password) < 7:
                message = 'Password must be at least 7 characters.'
                message_type = 'error'
            else:
                user.password = generate_password_hash(new_password)
                message = 'Password updated successfully.'
                message_type = 'success'

        #         # Handle profile picture upload
        # if 'profile_picture' in request.files:
        #     file = request.files['profile_picture']
        #     if file and allowed_file(file.filename):
        #         filename = secure_filename(file.filename)
        #         filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        #         file.save(filepath)
        #         user.profile_picture = filepath  # Save file path in database

        if not message_type == 'error':
            db.session.commit()
            message = 'Profile updated successfully.'
            message_type = 'success'
        
    return render_template('profile.html', user=current_user, message=message, message_type=message_type)

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
