"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db
from flask import Flask, render_template, redirect, request, flash, session

from model import User, Rating, Movie, connect_to_db, db

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""


    return render_template("homepage.html")

@app.route('/sign_in')
def sign_in():
    """Sign-in Page"""

    return render_template("signin_form.html")

@app.route('/process_signin',methods=["POST"])
def process_signin():
    """Process Sign In form"""

    input_username = request.form.get("username")
    input_password = request.form.get("password")

    user = User.query.filter(User.username==input_username,User.password==input_password).all()
    if input_username not in user:
        print "NOT HERE!!!!!!!!"
    print user

    # return render_template("process_signin.html",
    #                         username=input_username,
    #                         password=input_password)


@app.route('/users')
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
