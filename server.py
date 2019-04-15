from flask import Flask, request, redirect, render_template
import data_manager


app = Flask(__name__)

@app.route("/")
@app.route("/list")
def route_questions_list():
    pass


@app.route("/question/<question_id>")
def route_question_display(question_id):
    template_name = "question.html"
    question = data_manager.get_question_by_id(question_id)
    if question is None:
        return render_template(template_name, question_id=question_id)
    answers = data_manager.get_answers_by_question_id(question_id)
    return render_template(template_name, question=question, answers=answers)


@app.route("/add-question")
def route_question_add():
    pass


@app.route("/question/<question_id>/new-answer")
def route_post_answer(question_id):
    pass


if __name__ == "__main__":
    app.run(debug=True, port=5000)
