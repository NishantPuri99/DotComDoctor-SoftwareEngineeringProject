from flask_blog1.models import User,Post
from flask_blog1 import app, db, bcrypt
from flask import render_template, url_for, flash, redirect
from flask_blog1.forms import RegistrationForm,LoginForm
from flask_login import login_user, current_user
 
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
#     password = db.Column(db.String(60), nullable=False)
#     posts = db.relationship('Post', backref='author', lazy=True)

# def __repr__(self):
#     return f"User('{self.username}', '{self.email}', '{self.image_file}')"

# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.Text, nullable=False)
#     title = db.Column(db.String(100), nullable=False)
#     date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


# def __repr__(self):
#     return f"Post('{self.title}', '{self.date_posted}')"



posts = [
    {
        'author':'Nikhil Shaji',
        'datePosted': 'April 21st, 2020',
        'content':'This is the first post',
        'title':'Blog Post 1'
    },
    {
        'author':'Lanson Correa',
        'datePosted': 'April 22nd, 2020',
        'content':'This is the second post',
        'title':'Blog Post 2'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html' , posts=posts, title = 'Main')

@app.route("/about")
def about():
    return render_template('about.html' , title = 'About')

@app.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:  #This checks if a user is logged in, and prevents them from accessing the register page again
        return redirect(url_for('home'))
    form = RegistrationForm()
    if (form.validate_on_submit()):
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') #Hashing the password of thenew user
        user = User(username=form.username.data, email=form.email.data, password=hashed_password) #Creating a user
        db.session.add(user) #Adding user to database
        db.session.commit()
        flash("Account created successfully! Please Log In", 'success')
        return redirect(url_for('login'))
    return render_template('register.html' , title = 'Register', form=form)

@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated: #This checks if a user is logged in, and prevents them from accessing the register page again
        return redirect(url_for('home'))
    form = LoginForm()
    if (form.validate_on_submit()):
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Log In successful!.", 'success')
            return redirect(url_for('home'))
        else:
            flash("Log In unsuccessful. Please check email and password", 'danger')
    return render_template('login.html' , title = 'Login', form=form)


@app.route("/map") #Just testing the map
def map():
    return render_template('map.html' , posts=posts, title = 'Map')