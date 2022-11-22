import os 

from flask import Flask, session, request, render_template, redirect, flash, g
from sqlalchemy.exc import IntegrityError

from models import db, connect_db, User
from forms import UserAddForm, LoginForm, UpdateUserForm

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

# db.drop_all()
# db.create_all()

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
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                password=form.password.data,
                email=form.email.data,
                image_url=form.image_url.data or User.image_url.default.arg,
                bio=form.bio.data,
            )
            
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('user/signup.html', form=form)

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
        user = User.authenticate(form.username.data,
                                 form.password.data)

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
# Homepage

@app.route('/')
def homepage():
    """Render Homepage"""
    return render_template("home.html")

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
    form = UpdateUserForm()

    if form.validate_on_submit():
        user.username=form.username.data,
        user.first_name=form.first_name.data,
        user.last_name=form.last_name.data,
        user.password=form.password.data,
        user.email=form.email.data,
        user.image_url=form.image_url.data or User.image_url.default.arg,
        user.header_image_url=form.header_image_url.data or User.header_image_url.default.arg,
        user.bio=form.bio.data
        user.location=form.location.data
            
        db.session.commit()

        flash(f"Successfully updated {user.username}!", "success")
        return redirect(f"/profile")

    elif IntegrityError:
        # flash("Username already taken", 'danger')
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
