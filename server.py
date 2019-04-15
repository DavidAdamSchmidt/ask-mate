from flask import Flask, request, redirect, render_template
import data_manager


app = Flask(__name__)


@app.route("/list")
def route_questions_list():
    pass


@app.route("/question/<question_id>")
def route_question_display(question_id):
    template_name = "question.html"
    question = data_manager.get_question_by_id(question_id)
    if question is None:
        return render_template(template_name, question_id=question_id)
    question_headers = list(question.keys())
    data_manager.convert_headers_to_user_friendly(question_headers)
    answers = data_manager.get_answers_by_question_id(question_id)
    answer_headers = None
    if len(answers) > 0:
        answer_headers = list(answers[0].keys())
        data_manager.convert_headers_to_user_friendly(answer_headers)
    return render_template(
        template_name,
        question=question,
        question_headers=question_headers,
        answers=answers,
        answer_headers=answer_headers
    )


@app.route("/add-question")
def route_question_add():
    pass


@app.route("/question/<question_id>/new-answer")
def route_post_answer(question_id):
    pass


if __name__ == "__main__":
    app.run(debug=True, port=5000)
