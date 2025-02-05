from functools import wraps
from  flask import Flask, render_template, request, redirect, url_for, flash, session
from app import app,db
from models import User, Subject, Chapter, Quiz, Question, UserQuizAttempt
from datetime import datetime

# ============================= ALL HELPER FUNCTIONS ============================

# authentication for admin
def admin_auth_required(func):
    @wraps(func)
    @auth_required
    def inner(*args,**kwargs):
        if session['user_id'] != 1:
            flash('Access denied. Only admin can access this page.', category='danger')
            return redirect(url_for('home'))
        return func(*args, **kwargs)
    return inner

# authentication for user
def auth_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first.',category='danger')
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return inner

# ============================= ALL ROUTES =============================

# root landing page
@app.route('/')
def home():
    return render_template('landing.html',session=session)

# login get
@app.route('/login')
def login():
    return render_template('login.html')

# login post
@app.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    # checking if all fields are filled up
    if username=='' or password=='':
        flash('All fields are required', category='danger')
        return redirect(url_for('login'))
    
    # fetching user from db
    is_user = User.query.filter_by(username=username).first()
    
    # checking if user is admin and password is correct
    if username == 'admin@gmail.com' and password == 'admin':
        flash('Login successful as admin',category='success')
        session['user_id'] = is_user.id
        return redirect(url_for('adminDashboard'))
    
    if not is_user:
        flash('Username does not exist',category='danger')
        return redirect(url_for('signup'))
    if not is_user.check_password(password):
        flash('Incorrect password',category='danger')
        return redirect(url_for('login'))
    # login successful
    session['user_id'] = is_user.id
    return redirect(url_for('userDashboard'))

# signup get
@app.route('/signup')
def signup():
    return render_template('signup.html')

# signup post
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
        flash('All fields are required',category='danger')
        return redirect(url_for('signup'))
    # check if username already exists
    if User.query.filter_by(username=username).first():
        flash('This email has already been used earlier',category='danger')
        return redirect(url_for('signup'))
        
    new_user = User(username=username, password=password, name=name,qualification=qualification,dob=dob)
    db.session.add(new_user)
    db.session.commit()
    flash('User created successfully',category='success')
    return redirect(url_for('login'))

# logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('User logged out successfully',category='success')
    return redirect(url_for('home'))
    
# admin dashboard
@app.route('/adminDashboard')
@admin_auth_required
def adminDashboard():
    subjects = Subject.query.all()
    return render_template('subjects.html', subjects=subjects)

# user dashboard
@app.route('/userDashboard')
@auth_required
def userDashboard():
    return "hello"

# user profile
@app.route('/profile')
@auth_required
def userProfile():
    return render_template('userProfile.html', user=User.query.get(session['user_id']))

# ------------------------- SUBJECT CRUD -----------------------

# Add new Subject GET
@app.route('/addSubject')
@admin_auth_required
def addSubject():
    return render_template('addSubject.html')

# Add new Subject POST
@app.route('/addSubject', methods=['POST'])
@admin_auth_required
def addSubject_post():
    name = request.form.get('name')
    description = request.form.get('description')
    # checking if all fields are filled up
    if name=='' or description=='':
        flash('All fields are required', category='danger')
        return redirect(url_for('addSubject'))
    # check if subject already exists
    if Subject.query.filter_by(name=name).first():
        flash('The Subject is already present',category='danger')
        return redirect(url_for('addSubject'))
    new_subject = Subject(name=name, description=description)
    db.session.add(new_subject)
    db.session.commit()
    flash('Subject added successfully', category='success')
    return redirect(url_for('adminDashboard'))

# Delete Subject
@app.route('/adminDashboard/<subject_name>/delete/<int:subject_id>', methods=['POST'])
@admin_auth_required
def delete_Subject(subject_name, subject_id):
    subject = Subject.query.get(subject_id)
    if not subject:
        flash('Subject not found', category='danger')
        return redirect(url_for('adminDashboard'))
    
    # subject --> chapter --> quiz --> question
    
    # Fetching all chapters related to this subject
    chapters = Chapter.query.filter_by(subject_id=subject.id).all()
    for chapter in chapters:
        # Fetching all quizzes linked to this chapter
        quizzes = Quiz.query.filter_by(chapter_id=chapter.id).all()

        for quiz in quizzes:
            # Delete all questions related to this quiz
            Question.query.filter_by(quiz_id=quiz.id).delete()
            
            # Delete the quiz
            db.session.delete(quiz)

        # Delete the chapter
        db.session.delete(chapter)

    # Delete the subject itself
    db.session.delete(subject)
    db.session.commit()

    flash(f"Subject '{subject.name}' and all related data deleted successfully!", "success")
    return redirect(url_for('adminDashboard'))

# Edit Subject
@app.route('/adminDashboard/<subject_name>/edit_subject', methods=['GET','POST'])
@admin_auth_required
def edit_subject(subject_name):
    subject = Subject.query.filter_by(name=subject_name).first()
    if not subject:
        flash('Subject not found', category='danger')
        return redirect(url_for('adminDashboard'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        
        # checking if all fields are filled up
        if name=='' or description=='':
            flash('All fields are required', category='danger')
            return redirect(url_for('edit_subject', subject_name=subject_name))
        
        subject.name = name
        subject.description = description
        db.session.commit()
        flash(f"Subject '{subject.name}' updated successfully!", "success")
        return redirect(url_for('adminDashboard'))
    return render_template('editSubject.html', subject=subject)

# -----------------------------------------------------------------------

# ------------------------- CHAPTER CRUD------------------------


# Read all chapters
@app.route('/adminDashboard/<subject_name>')
@admin_auth_required
def chapter_list(subject_name):
    subject = Subject.query.filter_by(name=subject_name).first()
    if not subject:
        flash('Subject not found', category='danger')
        return redirect(url_for('adminDashboard'))
    chapter_list = subject.chapters
    return render_template('chapters.html', subject=subject, chapters=chapter_list)

# Add new Chapter GET
@app.route('/adminDashboard/<subject_name>/addChapter', methods=["GET","POST"])
@admin_auth_required
def addChapter(subject_name):
    subject = Subject.query.filter_by(name=subject_name).first()
    if not subject:
        flash('Subject not found', category='danger')
        return redirect(url_for('adminDashboard'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        
        # checking if all fields are filled up
        if name=='' or description=='':
            flash('All fields are required', category='danger')
            return redirect(url_for('addChapter', subject_name=subject_name))
        
        new_chapter = Chapter(name=name, description=description, subject_id=subject.id)
        db.session.add(new_chapter)
        db.session.commit()
        flash(f"Chapter '{new_chapter.name}' added successfully!", "success")
        return redirect(url_for('chapter_list', subject_name=subject_name))
    return render_template('addChapter.html', subject=subject)

# Delete Chapter
@app.route('/adminDashboard/delete/<chapter_name>/<int:chapter_id>', methods=['POST'])
@admin_auth_required
def delete_Chapter(chapter_name, chapter_id):
    chapter = Chapter.query.get(chapter_id)
    subject_name = chapter.subject.name
    if not chapter:
        flash('Chapter not found', category='danger')
        return redirect(url_for('chapter_list', subject_name=subject_name))
    
    # chapter --> quiz --> question
    
    # Fetching all quizzes related to this chapter
    quizzes = Quiz.query.filter_by(chapter_id=chapter.id).all()
    for quiz in quizzes:
        # Delete all questions related to this quiz
        Question.query.filter_by(quiz_id=quiz.id).delete()
        
        # Delete the quiz
        db.session.delete(quiz)
    
    # Delete the chapter
    db.session.delete(chapter)
    db.session.commit()

    flash(f"Chapter '{chapter.name}' and all related data deleted successfully!", "success")
    return redirect(url_for('chapter_list', subject_name=subject_name))

# Edit Chapter
@app.route('/adminDashboard/<subject_name>/<chapter_name>/edit_chapter', methods=['GET','POST'])
@admin_auth_required
def edit_chapter(subject_name, chapter_name):
    subject = Subject.query.filter_by(name=subject_name).first()
    chapter = Chapter.query.filter_by(name=chapter_name, subject_id=subject.id).first()
    if not chapter:
        flash('Chapter not found', category='danger')
        return redirect(url_for('chapter_list', subject_name=subject_name))
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        
        # checking if all fields are filled up
        if name=='' or description=='':
            flash('All fields are required', category='danger')
            return redirect(url_for('edit_chapter', subject_name=subject_name, chapter_name=chapter_name))
        
        chapter.name = name
        chapter.description = description
        db.session.commit()
        flash(f"Chapter '{chapter.name}' updated successfully!", "success")
        return redirect(url_for('chapter_list', subject_name=subject_name))
    return render_template('editChapter.html', chapter=chapter, subject=subject)

# -----------------------------------------------------------------------

# ------------------------- QUIZZES CRUD------------------------


# quiz read
@app.route('/adminDashboard/<subject_name>/<chapter_name>')
@admin_auth_required
def quizzes_list(chapter_name,subject_name):
    subject = Subject.query.filter_by(name=subject_name).first()
    chapter = Chapter.query.filter_by(name=chapter_name, subject_id=subject.id).first()
    if not subject or not chapter:
        flash('Subject or Chapter not found', category='danger')
        return redirect(url_for('adminDashboard'))
    quizzes = chapter.quizzes
    return render_template('quizzes.html', subject=subject, chapter=chapter, quizzes=quizzes)





# Define your 404 error handler
@app.errorhandler(404)
def not_found_error(error):
    return render_template('NotFound.html'), 404