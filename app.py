import os 

from flask import Flask, session, request, render_template, redirect, flash, g

from models import db, connect_db, User

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///natty_parks'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

app.app_context().push()

connect_db(app)

##############################################################################
# User signup/login/logout

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

##############################################################################
# Homepage

@app.route('/')
def homepage():
    """Render List Parks"""
    return render_template("pages/home.html", logged_in = True )

@app.route('/login-signup')
def login_signup():
    """Render User Login / Sign up Page"""
    return render_template("pages/login-signup.html")

@app.route('/profile')
def user_page():
    """Render Info / Edit page """
    return render_template("pages/user.html")

@app.route('/Park/<int:park_id>')
def park_info():
    """Render Park Information page"""
    return render_template("pages/park.html")

@app.errorhandler(404)
def NotFound(error):
    """Render a 404 Page"""
    print('error: ', error)
    return render_template("pages/not-found.html")
