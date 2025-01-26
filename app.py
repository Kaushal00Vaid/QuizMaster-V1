from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('landing.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

# Define your 404 error handler
@app.errorhandler(404)
def not_found_error(error):
    return render_template('NotFound.html'), 404

app.run(debug=True)