import os 

from flask import Flask, session, request, render_template, redirect, flash, g
from sqlalchemy.exc import IntegrityError

from models import db, connect_db, User
from forms import UserAddForm

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
db.drop_all()
db.create_all()

##############################################################################
# User signup/login/logout

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """User signup / Create user in db and redirect to home"""

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                image_url=form.image_url.data or User.image_url.default.arg,
                bio=form.bio.data,
            )
            
            db.session.commit()

        except IntegrityError:
            # flash("Username already taken", 'danger')
            return render_template('user/signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('users/signup.html', form=form)


##############################################################################
# Homepage

@app.route('/')
def homepage():
    """Render List Parks"""
    return render_template("home.html", logged_in = True )

##############################################################################
# 

@app.route('/profile')
def user_page():
    """Render Info / Edit page """
    return render_template("home.html")

@app.route('/Park/<int:park_id>')
def park_info():
    """Render Park Information page"""
    return render_template("home.html")

@app.errorhandler(404)
def NotFound(error):
    """Render a 404 Page"""
    print('error: ', error)
    return render_template("not_found.html")
