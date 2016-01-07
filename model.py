
##############################################################################
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



# This is the connection to the SQLite database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)
db = SQLAlchemy()

##############################################################################
class User(db.Model):
    __tablename__ = 'users'


    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    username = db.Column(db.String(20), nullable=True)
    question = db.Column(db.String(64))

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s email=%s>" % (self.user_id, self.email)

##############################################################################
# class User_Answer(db.Model):
#     __tablename__ = 'user_answers'

#     question_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
#     answer_id = db.Column(db.Integer, db.ForeignKey('answers.answer_id'), nullable=False)
#     questions = db.Column(db.String(64))
#     shake_type = db.Column(db.String(64))
#     user_count = db.Column(db.Integer)
#     answer_at = db.Column(db.DateTime)
#     question_count = db.Column(db.Integer)

#     user = db.relationship("User", backref=db.backref("user_answer", order_by=user_id))
#     answer = db.relationship("Answer", backref=db.backref("user_answer", order_by=answer_id))


#     def __repr__(self):
#         """Provide helpful representation when printed."""

#         return "<User_Answer user_answer_id=%s user_id=%s answer_id=%s>" % (self.user_answer_id, self.user_id, self.anwser_id)


##############################################################################

class Answer(db.Model):
    __tablename__ = 'answers'

    answer_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    answer = db.Column(db.String(64))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Answer answer_id=%s answer=%s>" % (self.answer_id, self.answer)

##############################################################################

def connect_to_db(app):
    """Connect the database to our Flask App"""
    # Configure to use our POSTGRES database
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgressql:///localhost/wdatabasedb'
   
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    db.app = app
    db.init_app(app)

##############################################################################


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from routes import app
    connect_to_db(app)
    print "Connected to DB."