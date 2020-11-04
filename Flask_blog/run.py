# from flask import Flask, render_template, url_for, flash, redirect
# from datetime import datetime
# from flask_sqlalchemy import SQLAlchemy 
# from forms import RegistrationForm,LoginForm


# app = Flask(__name__)
# app.config['SECRET_KEY'] = '6caa2c672d64ba7e2ba240bfdf6a009c'   #Use a random string of characters with secrets module. 
# app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
# db = SQLAlchemy(app)

# from models import User,Post

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



# posts = [
#     {
#         'author':'Nikhil Shaji',
#         'datePosted': 'April 21st, 2020',
#         'content':'This is the first post',
#         'title':'Blog Post 1'
#     },
#     {
#         'author':'Lanson Correa',
#         'datePosted': 'April 22nd, 2020',
#         'content':'This is the second post',
#         'title':'Blog Post 2'
#     }
# ]


# @app.route("/")
# @app.route("/home")
# def home():
#     return render_template('home.html' , posts=posts, title = 'Main')

# @app.route("/about")
# def about():
#     return render_template('about.html' , title = 'About')

# @app.route("/register", methods=['GET','POST'])
# def register():
#     form = RegistrationForm()
#     if (form.validate_on_submit()):
#         flash("Account created successfully!", 'success')
#         return redirect(url_for('home'))
#     return render_template('register.html' , title = 'Register', form=form)

# @app.route("/login", methods=['GET','POST'])
# def login():
#     form = LoginForm()
#     if (form.validate_on_submit()):
#         if form.email.data == 'admin@blog.com' and form.password.data == 'password':
#             flash("Log In successful!", 'success')
#             return redirect(url_for('home'))
#         else:
#             flash("Log In unsuccessful", 'danger')
#     return render_template('login.html' , title = 'Login', form=form)

from flask_blog1 import app #imports from __init__ file, since we're importing app, it has to exist in __init__.py


if __name__=='__main__':
    app.run(debug=True)