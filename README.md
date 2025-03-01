# QuizMaster-V1

**MAD-1 Project for Jan-2025 Term**

QuizMaster is a user-friendly quiz app designed to help users prepare for their exams across different courses, track their progress, and get detailed reviews based on their attempts.

---

## Features

- **User Authentication:** Login and Signup system for users.
- **Quiz Management:** Admin can create subjects, chapters, and quizzes.
- **CRUD Operations:** Admin can create, update, and delete quizzes.
- **Quiz Attempt & Review:** Users can attempt quizzes and track their progress.
- **Progress Tracking:** Users can review their past quiz attempts.
- **Search Functionality:** Users can search for quizzes based on subjects and chapters.

---

## Project Structure

```
QuizMaster/
│── instance/
│   ├── gradely.db  # SQLite database
│── static/
│   ├── assets/
│   ├── style.css  # Stylesheet
│── templates/  # HTML Templates
│── .env  # Environment variables
│── .gitignore  # Git ignore file
│── app.py  # Main Flask application
│── config.py  # Configuration settings
│── models.py  # Database models (SQLAlchemy)
│── routes.py  # Routes and application logic
│── README.md  # Project documentation
```

---

## Installation & Setup

### 1. Clone the Repository

```sh
git clone https://github.com/24f2000681/QuizMaster-V1.git
cd quizmaster
```

### 2. Create and Activate a Virtual Environment (Optional)

```sh
python -m venv venv
# Activate Virtual Environment:
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```sh
pip install -r requirements.txt
```

### 4. Run the Application

```sh
python app.py
```

The application will be available at: **http://127.0.0.1:5000/**

---

## License

This project is for educational purposes and follows an open-source license.

---

## Author

**Kaushal Vaid**
IITM BS Degree

For queries, reach out at **kaushalvaid123@gmail.com**.

---

Enjoy using **QuizMaster!** 🚀
