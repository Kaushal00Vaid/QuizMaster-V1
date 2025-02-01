from  flask import Flask, render_template, request, redirect, url_for, flash
from app import app,db
from models import User, Subject, Chapter, Quiz, Question, UserQuizAttempt

@app.route('/')
def home():
    return render_template('landing.html')

# login and signup
@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

# checking login credentials
@app.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    if username == 'admin@gmail.com' and password == 'admin':
        flash('Login successful as admin')
        return redirect(url_for('adminDashboard'))
    is_user = User.query.filter_by(username=username).first()
    if not is_user:
        flash('Username does not exist','danger')
        return redirect(url_for('signup'))
    if not is_user.check_password(password):
        flash('Incorrect password','danger')
        return redirect(url_for('login'))
    # login successful
    return redirect(url_for('userDashboard'))
    
# admin dashboard
@app.route('/adminDashboard')
def adminDashboard():
    return "admin"

# user dashboard
@app.route('/userDashboard')
def userDashboard():
    return "user"



# Define your 404 error handler
@app.errorhandler(404)
def not_found_error(error):
    return render_template('NotFound.html'), 404