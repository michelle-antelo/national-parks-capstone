import os 

from flask import Flask, session, request, render_template, redirect, flash, g, jsonify
from sqlalchemy.exc import IntegrityError
import requests

from models import db, connect_db, User
from forms import UserAddForm, LoginForm, UpdateUserForm

CURR_USER_KEY = "curr_user"

API_KEY = os.environ.get('API_KEY')
API_URL = os.environ.get('API_URL')
DATABASE_URL = os.environ.get('DATABASE_URL')
HEROKU_DATABASE_URL = os.environ.get('HEROKU_DATABASE_URL')

if HEROKU_DATABASE_URL.startswith("postgres://"):
    HEROKU_DATABASE_URL = HEROKU_DATABASE_URL.replace("postgres://", "postgresql://", 1)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', HEROKU_DATABASE_URL)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

app.app_context().push()

connect_db(app)

##############################################################################
# Homepage/Park Info

@app.route('/', methods=["GET", "POST"])
def homepage():
    """Home page lists parks"""

    search = request.args.get('q')

    if not search:
        resp = requests.get(
            f"{API_URL}/parks?api_key={API_KEY}",
            headers={"accept": "application/json"}
    )
        get_parks = resp.json()
        parks_list = get_parks['data']

    else:
        resp = requests.get(
            f"{API_URL}/parks?stateCode={search}",
            headers={"accept": "application/json"},
            params={'api_key': {API_KEY}, 'stateCode': '{search}'})

        get_parks = resp.json()
        parks_list = get_parks['data']

    return render_template("home.html", parks_list=parks_list)


@app.route('/info/<parkCode>', methods=["GET", "POST"])
def get_park(parkCode):
    res = requests.get(
        f"{API_URL}/parks?parkCode={parkCode}",
        headers={"accept": "application/json"},
        params={'api_key': {API_KEY}, 'parkCode': '{parkCode}'})

    get_park = res.json()
    park_info = get_park['data']
    
    return render_template('info.html', park_info=park_info)

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
                username=form.username.data.lower(),
                first_name=form.first_name.data.capitalize(),
                last_name=form.last_name.data.capitalize(),
                password=form.password.data,
                email=form.email.data.lower(),
                image_url=form.image_url.data or User.image_url.default.arg,
                bio=form.bio.data,
            )
            
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)

        flash(f"Hello, {user.first_name}!", "success")
        return redirect("/")

    else:
        return render_template('users/signup.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        print('Username: ', form.username.data, "Password? ", form.password.data)
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.first_name}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)

@app.route('/logout')
def logout():
    """Logout user"""

    do_logout()

    flash("Successfully logged out!", "success")
    return redirect("/")


##############################################################################
# View/edit profiles

@app.route('/profile')
def view_profile():
    """View user profile"""

    user = User.query.get(session[CURR_USER_KEY])

    return render_template("users/profile.html", user=user)

@app.route('/profile/edit', methods=["GET", "POST"])
def edit_profile():
    """Edit profile"""
    user = User.query.get(session[CURR_USER_KEY])
    form = UpdateUserForm(obj=user)

    if form.validate_on_submit():
        user.username=form.username.data.lower(),
        user.first_name=form.first_name.data.capitalize(),
        user.last_name=form.last_name.data.capitalize(),
        user.image_url=form.image_url.data or User.image_url.default.arg,
        user.location=form.location.data or User.location.default.arg,
        user.bio=form.bio.data
            
        db.session.commit()

        flash(f"Successfully updated {user.username}!", "success")
        return redirect(f"/profile")

    elif IntegrityError:
        return render_template('users/edit.html', form=form)

    else:
        return render_template('users/edit.html', form=form)

@app.route('/users')
def list_users():
    """Page with listing of users.

    Can take a 'q' param in querystring to search by that username.
    """

    search = request.args.get('q')

    if not search:
        users = User.query.all()
    else:
        users = User.query.filter(User.username.like(f"%{search}%")).all()

    return render_template('users/index.html', users=users)

@app.route('/users/<int:user_id>')
def users_show(user_id):
    """Show user profile."""

    user = User.query.get_or_404(user_id)

    return render_template('users/show.html', user=user)

##############################################################################
# Custom error handler

@app.errorhandler(404)
def NotFound(error):
    """Render a 404 Page"""
    print('error: ', error)
    return render_template("not_found.html")
