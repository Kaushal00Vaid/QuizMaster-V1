from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from config import Config
from dotenv import load_dotenv

# loading.env file for environment variables
load_dotenv()

app = Flask(__name__)

# loading config.py
app.config.from_object(Config)

# initialize SQLAlchemy
db = SQLAlchemy(app)

from routes import *


if __name__ == '__main__':
    app.run(debug=True)