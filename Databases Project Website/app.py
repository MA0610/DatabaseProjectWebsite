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


    
    
    if not Courses.query.first():   #populates the Courses table with values at app creation
        course_names = ["COMP 131","COMP 367", "COMP 373", "COMP 390", "COMP 490", "Personal Project"]
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
        db.session.commit()

     if not Project.query.first():   


        catWD = Category.query.filter_by(name="Web Development").all()
        catML = Category.query.filter_by(name="Machine Learning").all()
        catAI = Category.query.filter_by(name="AI").all()


        course_367 = Courses.query.filter_by(courseName="COMP 367").first()
        course_personal_project = Courses.query.filter_by(courseName="Personal Project").first()

        if not course_367 or not course_personal_project:
            raise ValueError("One or more courses are missing in the database.")

        projects_info = [
            Project(userName="Matthew Arboleda",
                    categories=catWD,  
                    course=course_367.id,  
                    description="This project is a scheduling website meant to help professors at Occidental communicate when each class should be to avoid having important classes at the same time before sending the schedule to the registrar's office. This website uses Python, SQLAlchemy, and Flask.",
                    githubLink="https://github.com/MA0610/SchedulingWebsite",
                    contributors="Diego Santiago, Jose Bustamente Ortiz, Marvin Romero",
                    postStatus="unapproved"),

            Project(userName="Matthew Arboleda",
                    categories=catWD,  
                    course=course_personal_project.id, 
                    description="This is an e-plant shopping website using REACT, this was made for IBM's developing front-end apps using REACT course.",
                    githubLink="https://github.com/MA0610/e-plantShopping",
                    contributors="",
                    postStatus="unapproved"),

            Project(userName="John Doe",
                    categories=catWD,  
                    course=course_personal_project.id,
                    description="A personal project to create a blog website using Flask and React.",
                    githubLink="https://github.com/johndoe/blog_website",
                    contributors="John Doe",
                    postStatus="unapproved"),


            Project(userName="Alice Smith",
                    categories=catML,  
                    course=course_367.id,
                    description="This is a project about Machine Learning for predictive analytics in healthcare.",
                    githubLink="https://github.com/alice/ml_healthcare_project",
                    contributors="Alice Smith, Bob Jones",
                    postStatus="unapproved"),



            Project(userName="Sarah Lee",
                    categories=catWD,  
                    course=course_367.id,
                    description="AI-based web application to optimize supply chain logistics.",
                    githubLink="https://github.com/sarahlee/ai_supply_chain",
                    contributors="Sarah Lee, Mark Zhang",
                    postStatus="unapproved"),
            
            Project(userName="Emily Chen",
            categories=catWD,
            course=course_personal_project.id,
            description="A web app for organizing and rating coffee shops using React and Firebase.",
            githubLink="https://github.com/emchen/coffee-rating-app",
            contributors="Emily Chen",
            postStatus="unapproved"),

            Project(userName="Jason Patel",
                    categories=catML,
                    course=course_367.id,
                    description="Machine learning project predicting student grades using scikit-learn.",
                    githubLink="https://github.com/jpatel/student-grade-predictor",
                    contributors="Nina Gomez",
                    postStatus="unapproved"),

            Project(userName="Olivia Brown",
                    categories=catAI,
                    course=course_personal_project.id,
                    description="An AI chatbot that helps students navigate course offerings.",
                    githubLink="https://github.com/oliviabrown/ai-coursebot",
                    contributors="Charlie Kim",
                    postStatus="unapproved"),

            Project(userName="Liam Nguyen",
                    categories=catWD,
                    course=course_367.id,
                    description="Event management site using Django, PostgreSQL, and Bootstrap.",
                    githubLink="https://github.com/lnguyen/event-site",
                    contributors="Sophia White",
                    postStatus="unapproved"),

            Project(userName="Sophia White",
                    categories=catML,
                    course=course_personal_project.id,
                    description="Python ML model to forecast stock prices using LSTM networks.",
                    githubLink="https://github.com/swhite/stock-forecast-lstm",
                    contributors="N/A",
                    postStatus="unapproved"),

            Project(userName="Noah Davis",
                    categories=catAI,
                    course=course_367.id,
                    description="AI-based personal fitness coach using OpenAI and wearable data.",
                    githubLink="https://github.com/ndavis/ai-fitness-coach",
                    contributors="Grace LeE",
                    postStatus="unapproved"),

            Project(userName="Mia Kim",
                    categories=catWD,
                    course=course_personal_project.id,
                    description="A portfolio website with dark mode and responsive design using HTML/CSS/JS.",
                    githubLink="https://github.com/miakim/portfolio-site",
                    contributors="N/A",
                    postStatus="unapproved"),

            Project(userName="Ethan Johnson",
                    categories=catML,
                    course=course_367.id,
                    description="Sentiment analysis on movie reviews using NLTK and logistic regression.",
                    githubLink="https://github.com/ejohnson/movie-review-sentiment",
                    contributors="N/A",
                    postStatus="unapproved"),

            Project(userName="Ava Garcia",
                    categories=catAI,
                    course=course_personal_project.id,
                    description="Voice-controlled smart home assistant built with Python and Raspberry Pi.",
                    githubLink="https://github.com/agarcia/smart-home-ai",
                    contributors="N/A",
                    postStatus="unapproved"),

            Project(userName="Lucas Walker",
                    categories=catWD,
                    course=course_367.id,
                    description="Collaborative note-taking web app using Flask and Socket.IO.",
                    githubLink="https://github.com/lwalker/note-collab",
                    contributors="Mia Kim",
                    postStatus="unapproved"),
                Project(userName="Grace Lee",
                    categories=catML,
                    course=course_personal_project.id,
                    description="A TensorFlow-powered handwriting recognition app.",
                    githubLink="https://github.com/gracelee/handwriting-ml",
                    contributors="N/A",
                    postStatus="unapproved"),

            Project(userName="Benjamin Harris",
                    categories=catAI,
                    course=course_367.id,
                    description="Facial recognition security system using OpenCV and AI.",
                    githubLink="https://github.com/bharris/facial-recognition-security",
                    contributors="N/A",
                    postStatus="unapproved"),

            Project(userName="Ella Moore",
                    categories=catWD,
                    course=course_personal_project.id,
                    description="Recipe sharing website using Node.js and Express.",
                    githubLink="https://github.com/ellamoore/recipe-share",
                    contributors="N/A",
                    postStatus="unapproved"),

            Project(userName="Alexander Wright",
                    categories=catML,
                    course=course_367.id,
                    description="Predicting air quality index using machine learning and real-time sensor data.",
                    githubLink="https://github.com/awright/air-quality-ml",
                    contributors="N/A",
                    postStatus="unapproved"),

            Project(userName="Isabella Thompson",
                    categories=catAI,
                    course=course_personal_project.id,
                    description="Natural language processor that summarizes articles.",
                    githubLink="https://github.com/isabellat/nlp-summarizer",
                    contributors="N/A",
                    postStatus="unapproved"),

            Project(userName="Michael Robinson",
                    categories=catWD,
                    course=course_367.id,
                    description="An online bookstore built with Flask and SQLAlchemy.",
                    githubLink="https://github.com/mrobinson/bookstore-app",
                    contributors="N/A",
                    postStatus="unapproved"),

            Project(userName="Charlotte Perez",
                    categories=catML,
                    course=course_personal_project.id,
                    description="ML-based medical diagnosis support system.",
                    githubLink="https://github.com/charlotteperez/medical-ml",
                    contributors="N/A",
                    postStatus="unapproved"),

            Project(userName="Henry Young",
                    categories=catAI,
                    course=course_367.id,
                    description="An AI that plays chess using the Minimax algorithm.",
                    githubLink="https://github.com/hyoung/chess-ai",
                    contributors="N/A",
                    postStatus="unapproved"),

            Project(userName="Amelia Adams",
                    categories=catWD,
                    course=course_personal_project.id,
                    description="A responsive travel blog template using HTML5 and Tailwind CSS.",
                    githubLink="https://github.com/ameliaadams/travel-blog",
                    contributors="Henry Young",
                    postStatus="unapproved"),

            Project(userName="Daniel Scott",
                    categories=catML,
                    course=course_367.id,
                    description="Crime pattern analysis using unsupervised clustering techniques.",
                    githubLink="https://github.com/dscott/crime-analysis-ml",
                    contributors="Emily Chen",
                    postStatus="unapproved"),

            Project(userName="Natalie Brooks",
                    categories=catAI,
                    course=course_personal_project.id,
                    description="An AI scriptwriting tool that generates short stories using GPT APIs.",
                    githubLink="https://github.com/nbrooks/ai-storygen",
                    contributors="N/A",
                    postStatus="unapproved"),

            Project(userName="Zachary Hill",
                    categories=catWD,
                    course=course_367.id,
                    description="A fully functional to-do list app using Vue.js and Firebase.",
                    githubLink="https://github.com/zhill/todo-vue-app",
                    contributors="John Hill",
                    postStatus="unapproved"),

            Project(userName="Jasmine Reed",
                    categories=catML,
                    course=course_personal_project.id,
                    description="ML model for predicting energy usage in smart homes.",
                    githubLink="https://github.com/jreed/energy-ml-predictor",
                    contributors="Sue Reed",
                    postStatus="unapproved"),

            Project(userName="Leo Martinez",
                    categories=catAI,
                    course=course_367.id,
                    description="AI virtual assistant that schedules meetings and reminders.",
                    githubLink="https://github.com/leom/ai-assistant",
                    contributors="Alice Smith",
                    postStatus="unapproved"),

            Project(userName="Brooklyn Scott",
                    categories=catWD,
                    course=course_personal_project.id,
                    description="Photography portfolio website with dynamic galleries using React.",
                    githubLink="https://github.com/bscott/photo-gallery",
                    contributors="N/A",
                    postStatus="unapproved"),

            Project(userName="Owen Turner",
                    categories=catML,
                    course=course_367.id,
                    description="Predictive analytics for NBA player performance.",
                    githubLink="https://github.com/oturner/nba-predictor",
                    contributors="Ethan Johnson",
                    postStatus="unapproved"),

            Project(userName="Claire Bennett",
                    categories=catAI,
                    course=course_personal_project.id,
                    description="AI for adaptive music generation based on user emotion.",
                    githubLink="https://github.com/clairebennett/ai-music-emotion",
                    contributors="N/A",
                    postStatus="unapproved"),

            Project(userName="Logan Carter",
                    categories=catWD,
                    course=course_367.id,
                    description="A car dealership inventory system built with Django.",
                    githubLink="https://github.com/lcarter/dealer-inventory",
                    contributors="N/A",
                    postStatus="unapproved"),

            Project(userName="Victoria Cruz",
                    categories=catML,
                    course=course_personal_project.id,
                    description="Deep learning CNN to classify x-ray images.",
                    githubLink="https://github.com/vcruz/xray-classification",
                    contributors="James Cruz",
                    postStatus="unapproved"),

            Project(userName="Ryan Bell",
                    categories=catAI,
                    course=course_367.id,
                    description="An AI-powered recipe recommender based on fridge contents.",
                    githubLink="https://github.com/rbell/ai-recipe-helper",
                    contributors="Ava Garcia",
                    postStatus="unapproved"),

            Project(userName="Samantha Evans",
                    categories=catWD,
                    course=course_personal_project.id,
                    description="A personal budgeting app built with React Native for mobile devices.",
                    githubLink="https://github.com/sevans/budget-buddy",
                    contributors="Chris Evans",
                    postStatus="unapproved"),

            Project(userName="Dylan Rivera",
                    categories=catML,
                    course=course_367.id,
                    description="Real estate price prediction using regression models.",
                    githubLink="https://github.com/drivera/real-estate-predictor",
                    contributors="Jane Rivera",
                    postStatus="unapproved"),

            Project(userName="Hailey Morgan",
                    categories=catAI,
                    course=course_personal_project.id,
                    description="Chatbot for language learning using BERT and conversation trees.",
                    githubLink="https://github.com/hmorgan/language-bot",
                    contributors="N/A",
                    postStatus="unapproved"),

            Project(userName="Nathan Powell",
                    categories=catWD,
                    course=course_367.id,
                    description="A bike rental service website using Angular and Firebase.",
                    githubLink="https://github.com/npowell/bike-rental-app",
                    contributors="Norman Powell",
                    postStatus="unapproved"),

            Project(userName="Madeline Hayes",
                    categories=catML,
                    course=course_personal_project.id,
                    description="Breast cancer diagnosis classifier using SVM and sklearn.",
                    githubLink="https://github.com/mhayes/breast-cancer-ml",
                    contributors="N/A",
                    postStatus="unapproved"),

            Project(userName="Cole Bennett",
                    categories=catAI,
                    course=course_367.id,
                    description="AI-powered resume analyzer that scores based on job descriptions.",
                    githubLink="https://github.com/cbennett/resume-ai",
                    contributors="N/A",
                    postStatus="unapproved"),

            Project(userName="Kayla Simmons",
                    categories=catWD,
                    course=course_personal_project.id,
                    description="An online bookstore UI clone built with Bootstrap and jQuery.",
                    githubLink="https://github.com/ksimmons/bookstore-clone",
                    contributors="Steven Simmons",
                    postStatus="unapproved"),

            Project(userName="Hunter Moore",
                    categories=catML,
                    course=course_367.id,
                    description="Traffic prediction system using historical and weather data.",
                    githubLink="https://github.com/hmoore/traffic-predictor",
                    contributors="Hunter Jones",
                    postStatus="unapproved"),

            Project(userName="Kaitlyn Foster",
                    categories=catAI,
                    course=course_personal_project.id,
                    description="AI poetry generator using LSTM networks and classic poems.",
                    githubLink="https://github.com/kfoster/poetry-generator",
                    contributors="Dexter Foster",
                    postStatus="unapproved"),

            Project(userName="Blake Ramirez",
                    categories=catWD,
                    course=course_367.id,
                    description="E-commerce site template with shopping cart and checkout flow.",
                    githubLink="https://github.com/ramirezblake/ecommerce-template",
                    contributors="Blake Griffin",
                    postStatus="unapproved"),

            Project(userName="Aiden Walker",
                    categories=catML,
                    course=course_personal_project.id,
                    description="Sentiment analysis on social media posts using BERT and Hugging Face.",
                    githubLink="https://github.com/awalker/social-media-sentiment",
                    contributors="Adrien Walker",
                    postStatus="unapproved"),

            Project(userName="Sophia Harris",
                    categories=catAI,
                    course=course_367.id,
                    description="AI for automatic image captioning using convolutional neural networks.",
                    githubLink="https://github.com/sharris/image-captioning-ai",
                    contributors="N/A",
                    postStatus="unapproved"),

            Project(userName="Landon Nelson",
                    categories=catWD,
                    course=course_personal_project.id,
                    description="A mobile-first weather app with real-time API integration using React.",
                    githubLink="https://github.com/lnelson/weather-app",
                    contributors="N/A",
                    postStatus="unapproved"),

            Project(userName="Madison Clark",
                    categories=catML,
                    course=course_367.id,
                    description="Customer churn prediction model for a subscription-based business.",
                    githubLink="https://github.com/mclark/churn-predictor",
                    contributors="John Martinez",
                    postStatus="unapproved"),

            Project(userName="Luke Martinez",
                    categories=catAI,
                    course=course_personal_project.id,
                    description="AI-based document summarizer for research papers.",
                    githubLink="https://github.com/lmartinez/ai-doc-summarizer",
                    contributors="Luke Garza",
                    postStatus="unapproved"),

            Project(userName="Maya Turner",
                    categories=catWD,
                    course=course_367.id,
                    description="Personal fitness tracker app with data visualization using JavaScript.",
                    githubLink="https://github.com/mturner/fitness-tracker",
                    contributors="Timmy Turner",
                    postStatus="unapproved"),

            Project(userName="Eli James",
                    categories=catML,
                    course=course_personal_project.id,
                    description="Predicting housing prices using XGBoost and historical sales data.",
                    githubLink="https://github.com/ejames/housing-price-predictor",
                    contributors="James Eli",
                    postStatus="unapproved"),

            Project(userName="Lila Cooper",
                    categories=catAI,
                    course=course_367.id,
                    description="AI-driven language translator that supports real-time conversation.",
                    githubLink="https://github.com/lcooper/ai-translator",
                    contributors="Sheldon Cooper",
                    postStatus="unapproved"),

            Project(userName="Mason Graham",
                    categories=catWD,
                    course=course_personal_project.id,
                    description="Recipe generator app based on ingredients in the fridge.",
                    githubLink="https://github.com/masongraham/recipe-generator",
                    contributors="N/A",
                    postStatus="unapproved"),

            Project(userName="Zoey Roberts",
                    categories=catML,
                    course=course_367.id,
                    description="ML algorithm to detect fake news from news articles.",
                    githubLink="https://github.com/zroberts/fake-news-detection",
                    contributors="N/A",
                    postStatus="unapproved")
        ]

        

        # Bulk insert the projects into the database
      
        for values in projects_info:
                db.session.add(values)
        db.session.commit()  


        

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
