from functools import wraps
from  flask import Flask, render_template, request, redirect, url_for, flash, session
from app import app,db
from models import User, Subject, Chapter, Quiz, Question, UserQuizAttempt
from datetime import datetime

# authentication for admin
def admin_auth_required(func):
    @wraps(func)
    @auth_required
    def inner(*args,**kwargs):
        if session['user_id'] != 1:
            flash('Access denied. Only admin can access this page.')
            return redirect(url_for('home'))
        return func(*args, **kwargs)
    return inner

# authentication for user
def auth_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first.')
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return inner


@app.route('/')
@auth_required
def home():
    return render_template('landing.html', name=User.query.get(session['user_id']))

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
    # checking if all fields are filled up
    if username=='' or password=='':
        flash('All fields are required')
        return redirect(url_for('login'))
    
    # fetching user from db
    is_user = User.query.filter_by(username=username).first()
    
    # checking if user is admin and password is correct
    if username == 'admin@gmail.com' and password == 'admin':
        flash('Login successful as admin','success')
        session['user_id'] = is_user.id
        return redirect(url_for('home'))
    
    if not is_user:
        flash('Username does not exist','danger')
        return redirect(url_for('signup'))
    if not is_user.check_password(password):
        flash('Incorrect password','danger')
        return redirect(url_for('login'))
    # login successful
    session['user_id'] = is_user.id
    return redirect(url_for('home'))

# signup details and updation in DB
@app.route('/signup',methods=['POST'])
def signup_post():
    username = request.form.get('username')
    password = request.form.get('password')
    name = request.form.get('name')
    qualification = request.form.get('qualification')
    # handling dates
    dob_string = request.form.get('dob')
    dob = datetime.strptime(dob_string, '%Y-%m-%d').date()
    
    # checking if all fields are filled up
    if username=='' or password=='' or name=='' or qualification=='' or dob=='':
        flash('All fields are required')
        return redirect(url_for('signup'))
    # check if username already exists
    if User.query.filter_by(username=username).first():
        flash('This email has already been used earlier')
        return redirect(url_for('signup'))
        
    new_user = User(username=username, password=password, name=name,qualification=qualification,dob=dob)
    db.session.add(new_user)
    db.session.commit()
    flash('User created successfully','success')
    return redirect(url_for('login'))

# logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))
    
# admin dashboard
@app.route('/adminDashboard')
@admin_auth_required
def adminDashboard():
    return "admin"

# user dashboard
@app.route('/profile')
@auth_required
def userProfile():
    return render_template('userProfile.html', user=User.query.get(session['user_id']))



# Define your 404 error handler
@app.errorhandler(404)
def not_found_error(error):
    return render_template('NotFound.html'), 404