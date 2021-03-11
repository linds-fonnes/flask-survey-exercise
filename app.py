from flask import Flask, request, render_template, redirect, flash, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey


app = Flask(__name__)
app.config["SECRET_KEY"] = "secret-secret-secret"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

questions = survey.questions

@app.route("/session_response", methods=["POST"])
def set_reponses():
    session["responses"] = []
    return redirect("/questions/0")

@app.route("/")
def show_survey():
    title = survey.title
    instructions = survey.instructions
    return render_template("start.html", title=title,instructions=instructions)

@app.route("/questions/<int:num>")
def show_question(num):
    responses = session["responses"]

    if len(responses) != num:
        flash("Stop messing around! Invalid question")
        return redirect(f"/questions/{len(responses)}")

    elif len(responses) == len(questions):
        return redirect("/thank_you")

    return render_template("question.html",questions=questions,num=num)
    
@app.route("/answers", methods=["POST"])
def add_answer():
    answer = request.form.get("choice_val")
    
    responses = session["responses"]
    responses.append(answer)
    session["responses"] = responses

    if len(responses) == len(questions):
        return redirect("/thank_you")

    elif len(responses) < len(questions):
        return redirect(f"/questions/{len(responses)}")

@app.route("/thank_you")
def thanks():
    return render_template("thank_you.html")