from flask import *
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "shhhh"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False



responses = []


@app.route('/')
def show_survey_start():
    """shows survey title and instructions"""

    return render_template("survey_start.html", survey=survey)



@app.route('/begin', methods=['POST'])
def begin_survey():
    """starts the survey"""

    return redirect("/questions/0")



@app.route('/answers', methods=['POST'])
def handle_question():
    """updates responses and redirects to next question"""

    choice = request.form["answer"]

    responses.append(choice)

    if (len(responses) == len(survey.questions)):
        return redirect("/complete")
    else:
        return redirect(f"/questions/{len(responses)}")



@app.route('/questions/<int:qid>')
def show_question(qid):
    """shows current question"""

    if (responses is None):
        return redirect("/")
    
    if (len(responses) == len(survey.questions)):
        return redirect("/complete")
    
    if (len(responses) != qid):
        flash('NO SKIPPING QUESTIONS!!')
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[qid]
    return render_template("question.html", question_num=qid, question=question)
    


@app.route('/complete')
def complete():
    """shows thank you page"""

    return render_template("thank_you.html")
