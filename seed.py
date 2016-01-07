from model import connect_to_db, db
from model import Answer
from routes import app
###############################################################################


def debug():
    """ return message in the console if data loaded successfully"""

    msg = "wanderlust db is seeded"

    print msg
###############################################################################



def load_answers():
    # open csv file (us_states)
    answer_file = open("static/data/answer.txt")
    #read each line
    for line in answer_file:
        # split on ","   --> list
        line_list = line.split("|")
        # each item in list -->  remove whitespace .strip()
        for i in range(len(line_list)):
            line_list[i] = line_list[i].strip()

        answer_id, answer = line_list[0], line_list[1]
        print "ANSWER_ID: %s ANSWER: %s" % (answer_id, answer)
        # # make State(....) object
        answer = Answer(answer_id=answer_id, answer=answer)

        # add to session
        db.session.add(answer)
        # commit session
    db.session.commit()

    debug()
    
###############################################################################
                            # HELPER FUNCTION #
###############################################################################

if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_answers()