from flask import Flask, request, jsonify, render_template, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Project, User

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


# User loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/submitProject')
@login_required
def submit():
    return render_template('submit.html')


@app.route('/grabProject', methods=['GET'])
def getProject():
    return jsonify()


@app.route('/putProject', methods=['POST'])
def putProject():
    data = request.json

    projectUser = data.get('projectAuthor')
    projectCategories = data.get('projectCategories')
    projectDescription = data.get('projectDescription')
    projectLink = data.get('projectLink')

    newProject = Project(
        userName=projectUser,
        categories=projectCategories,
        description=projectDescription,
        githubLink=projectLink
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

    return jsonify(allProjects)

@app.route('/testUsers', methods=['GET'])
def testUsers():
    allUsers = []

    userValues = User.query.all()

    for users in userValues:
        user_data = {
            "id": users.id,
            "name": users.first_name,
            "email": users.email,
            "password": users.password

        }

        allUsers.append(user_data)

    return jsonify(allUsers)





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
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # Validation
        if User.query.filter_by(email=email).first():
            message = 'Email already in use.'
            message_type = 'error'
        elif len(email) < 4:
            message = 'Email must be greater than 3 characters.'
            message_type = 'error'
        elif len(first_name) < 2:
            message = 'First name must be greater than 1 character.'
            message_type = 'error'
        elif password1 != password2:
            message = 'Passwords don\'t match.'
            message_type = 'error'
        elif len(password1) < 7:
            message = 'Password must be at least 7 characters.'
            message_type = 'error'
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            message = 'Account created successfully!'
            message_type = 'success'
            login_user(new_user, remember=True)
            
            flash('Created account sucessfully!', category='success') #DOESN"T WORK YET

            return redirect(url_for('index'))  # Redirect to home page

    return render_template("sign-up.html", user=current_user, message=message, message_type=message_type)



if __name__ == '__main__':
    app.run(debug=True)
