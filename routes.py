##############################################################################
                ##### CONTROLLER, ROUTES, VIEW  ####
##############################################################################
from flask import Flask
from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_wtf import Form
from jinja2 import StrictUndefined
from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.openid import OpenID
from model import User, Answer
import random
import time
from model import connect_to_db, db

################################################################################

app = Flask(__name__)

app.secret_key = 'LEGENDARY'
app.jinja_env.undefined = StrictUndefined

################################################################################
                            ##### ROUTES  ####
################################################################################
@app.route('/test')
def test():
    """Show login form."""

    return render_template("test.html")


################################################################################
                            ## LOGIN PROCESS ##

@app.route('/', methods=['GET'])
def index():
    """Show login form."""

    return render_template("index.html")


@app.route('/login-process', methods=['POST'])
def process_login():
    """Log user into site, find user in the DB and their
    their user id in the session then if they
     are logged in redirect them to map page"""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]

    # printing data from form to BASH
    print "form password"

    print password

    # check user exisit and then asign them variable user
    user = User.query.filter_by(email=email).first()

    print "\n \n \n ", user

    # Conditions
    if not user:

        flash("No such user")

        return redirect("/")

    elif user.password != password:

        flash("Incorrect password")

        return redirect("/")
    else:
        session["user_id"] = user.user_id

    flash("Logged in")

    return redirect('/decisions')

##############################################################################
                        ## LOG OUT ROUTE ##
##############################################################################

@app.route("/logout")
def process_logout():
    """removing user_id from session to logout user"""

    print " LOGGED OUT USER "

    del session["user_id"]

    flash("You have Successfully Logged Out!")

    return redirect("/")

##############################################################################
                            # # REGISTER ROUTE # #
##############################################################################


@app.route('/register-process', methods=['POST'])
def register_processed():
    """New user signup form"""

    print "REGISTER ROUTE IS WORKING"

    # Get variables from HTML form
    email = request.form["email"]

    password = request.form["password"]

    # query the DB for user
    new_user = User(email=email, password=password)

    # check DB for user searching by email
    same_email_user = User.query.filter(User.email == email).first()

    # users who registered / login will be redircted --> passport/profile pg.
    if same_email_user:
        flash("Email is already registered. Please signin to your account")
        return redirect("/")

    # check user by username --> condition to authentiate user
    same_username = User.query.filter(User.email == email).first()
    if same_username:
        flash("please pick another username")
        return redirect("/")

        # add user to db if they are new
    db.session.add(new_user)
        # commit transaction
    db.session.commit()

    # query db user by email add them to current session and redirect
    # user to passport page

    user = User.query.filter_by(email=email).first()

    flash("User %s added.You have successfully created an account! Welcome to Wanderlust" % email)

    session["user_id"] = user.user_id

    return redirect("/index")



################################################################################

# @app.route('/question-ajax-add', methods=["POST"])
# def answers():
#     answer_list = []
#     random_list = random.choice(list)
#     return random_list

# def question():
#     user_input = raw_input("what is your question")

# AJAX CALL

# @app.route('/question-ajax-add', methods=["POST"])
# def magic():
#     """magic 8 ball"""
#     user_id = session["user_id"]
#      # input from ajax call from HTML form
#      question = request.form.get('question', None)
#      print 'question-ajax-add', answer
#      user = db.session.query(User).filter_by(user_id=user_id).one()
#      user.question = first

#     # commit form information to Database
#     db.session.commit()

#     user_question_data = {"question": question}


#     print "Question has been stored in Database."

#  return jsonify(user_question_data)

##############################################################################

# HELPER FUNCTIONS
##############################################################################



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    app.debug = True
    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    app.run()