from flask_sqlalchemy import SQLAlchemy
from app import db,app
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# models
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(512), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    qualification = db.Column(db.String(60), nullable=False)
    dob = db.Column(db.Date, nullable=False)
# inserting admin
def insert_admin(*args, **kwargs):
    if not User.query.filter_by(username="admin@gmail.com").first():
        admin = User(
            username="admin@gmail.com",
            password="admin",
            name="Admin",
            qualification="Admin",
            dob=datetime.strptime("2005-08-29", "%Y-%m-%d").date()
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin Added")
    else:
        print("Admin already exists")

# checking password
def check_password(self, password):
    return check_password_hash(self.password, password)


class Subject(db.Model):
    __tablename__ ='subject'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

class Chapter(db.Model):
    __tablename__ ='chapter'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)

    subject = db.relationship('Subject', backref=db.backref('chapters', lazy=True))

class Quiz(db.Model):
    __tablename__ ='quiz'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    duration = db.Column(db.Integer, nullable=False, default=10)

    chapter = db.relationship('Chapter', backref=db.backref('quizzes', lazy=True))

class Question(db.Model):
    __tablename__ ='question'
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    questionTitle = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(255), nullable=False)
    option_b = db.Column(db.String(255), nullable=False)
    option_c = db.Column(db.String(255), nullable=False)
    option_d = db.Column(db.String(255), nullable=False)
    correct_option = db.Column(db.String(1), nullable=False) # 'A', 'B', 'C', 'D'
    marks = db.Column(db.Integer, nullable=False)

    quiz = db.relationship('Quiz', backref=db.backref('questions', lazy=True))


class UserQuizAttempt(db.Model):
    __tablename__ ='user_quiz_attempt'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False, default=0)

    user = db.relationship('User', backref=db.backref('quiz_attempts', lazy=True))
    quiz = db.relationship('Quiz', backref=db.backref('attempts', lazy=True))

# creating tables
def create_tables():
    with app.app_context():
        db.create_all()
        insert_admin()

create_tables()