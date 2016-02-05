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

    # checking to see if we have an account with the user's inputted email and password
    user_list = User.query.filter(User.email==input_username,User.password==input_password).all()
    # 
    # if we didn't find any user by that name and email 
    if user_list == []:
        # create new user and adding to database
        new_user = User(email=input_username,password=input_password)
        db.session.add(new_user)
        db.session.commit() #the database gives the user its user id at this point
        user_id = new_user.user_id
        session["user_id"] = user_id
        print "ADDED TO DB"
    else:
        # our user exists
        print "YOUR USER EXISTS!!!!" #put in flash message and redirect to new page
        # 
        user_id = user_list[0].user_id
        session["user_id"] = user_id # logging the user in
        flash("Successfuly logged in")

    return redirect("/")

    user_id = user_list[0]

@app.route('/logged_out')
def logged_out():
    """Log out user"""

    del session["user_id"]
    flash("Successfuly logged out")

    return redirect("/")


@app.route('/users')
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route('/user_details')
def user_demographics():

    return render_template()


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
