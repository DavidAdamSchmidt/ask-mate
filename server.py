from flask import Flask, request, redirect, render_template, url_for
import data_manager
import time


app = Flask(__name__)


@app.route("/")
@app.route("/list")
def route_questions_list():
    id_type = request.args.get("order_by")
    if not id_type:
        id_type = "submission_time"
    direction_ = request.args.get("order_direction")
    direction_ = True if direction_ == "asc" else False
    question_list = data_manager.sort_by_any("data/question.csv", id_type, direction_)
    return render_template('index.html', question_list=question_list, current_dir=direction_)


@app.route("/question/<question_id>/vote-<operation>")
def route_question_votes(question_id, operation):
    increase_by = 1 if operation == "up" else -1
    data_manager.update_vote_number(question_id, increase_by)
    return redirect("/")


@app.route("/answer/<answer_id>/vote-<operation>")
def route_answer_votes(answer_id, operation):
    increase_by = 1 if operation == "up" else -1
    data_manager.update_vote_number(answer_id, increase_by, answer=True)
    answer = data_manager.get_record_by_id(answer_id, answer=True)
    return redirect(url_for("route_question_display", question_id=answer["question_id"]))


@app.route("/question/<question_id>")
def route_question_display(question_id):
    template_name = "question.html"
    question = data_manager.get_record_by_id(question_id)
    if question is None:
        return render_template(template_name, question_id=question_id)
    answers = data_manager.get_answers_by_question_id(question_id)
    return render_template(template_name, question=question, answers=answers)


@app.route("/question/<question_id>/edit", methods=['GET', 'POST'])
def route_question_edit(question_id):
    if request.method == 'POST':
        new_q = request.form.to_dict()
        new_q['submission_time'] = int(time.time())
        headers = data_manager.QUESTIONS_HEADER

        data_manager.update_to_csv('data/question.csv', new_q, headers)
        return redirect('/question/%s' % question_id)
    question = data_manager.get_question_by_id(question_id)
    if question is None:
        return render_template('question.html', question_id=question_id)
    else:
        return render_template('add_question.html', question=question)


@app.route("/question/<question_id>/new-answer", methods=["GET", "POST"])
def route_add_answer(question_id):
    if request.method == "POST":
        new_answer = request.form.to_dict()
        new_answer["id"] = len(data_manager.read_csv("data/answer.csv"))
        new_answer["submission_time"] = int(time.time())
        new_answer["vote_number"] = "0"
        new_answer["question_id"] = question_id
        headers = data_manager.ANSWERS_HEADER
        data_manager.write_new_to_csv("data/answer.csv", headers, new_answer)
        return redirect(f"/question/{question_id}")
    return render_template("add_answer.html", question_id=question_id)


@app.route("/add-question", methods=['GET', 'POST'])
def route_question_add():
    id = len(data_manager.read_csv('data/question.csv'))
    if request.method == 'POST':
        new_q = request.form.to_dict()
        new_q['submission_time'] = int(time.time())
        headers = data_manager.QUESTIONS_HEADER
        
        data_manager.write_new_to_csv('data/question.csv', headers, new_q)
        return redirect('/question/%s' % id)
    else:
        return render_template('add_question.html', id=id)


if __name__ == "__main__":
    app.run(debug=True, port=2000)
