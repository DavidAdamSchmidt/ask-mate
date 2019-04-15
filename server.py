from flask import Flask, request, redirect, render_template


app = Flask(__name__)


@app.route("/list")
def route_questions_list():
    pass


@app.route("/question/<question_id")
def route_question_disp(question_id):
    pass


@app.route("/add-question")
def route_question_add():
    pass


@app.route("/question/<question_id>/new-answer")
def route_post_answer(question_id):
    pass


if __name__ == "__main__":
    app.run(debug=True, port=5000)
