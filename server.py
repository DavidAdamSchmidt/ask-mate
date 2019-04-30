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
    limit = 5 if request.path == '/' else None
    question_list = data_manager.sort_by_any('question', id_type, direction_, limit)
    return render_template('index.html', question_list=question_list, current_dir=direction_)


@app.route("/question/<question_id>/vote-<operation>", methods=["GET", "POST"])
def route_question_votes(question_id, operation):
    if request.method == "POST":
        op_change = '+1' if operation == "up" else '-1'
        data_manager.update_vote_number('question', op_change, question_id)
    return redirect("/")


@app.route("/answer/<answer_id>/vote-<operation>",  methods=["GET", "POST"])
def route_answer_votes(answer_id, operation):
    if request.method == "POST":
        op_change = '+1' if operation == "up" else '-1'
        data_manager.update_vote_number('answer', op_change, answer_id)
        answer = data_manager.get_record_by_id(answer_id, answer=True)
        return redirect(url_for("route_question_display", question_id=answer["question_id"]))
    return redirect("")


@app.route("/question/<question_id>", methods=['GET', 'POST'])
def route_question_display(question_id):
    if request.method == 'POST':
        new_q = request.form.to_dict()
        new_q['submission_time'] = int(time.time())
        headers = data_manager.QUESTIONS_HEADER

        data_manager.update_to_csv('data/question.csv', new_q, headers)
        return redirect('/question/%s' % question_id)
    template_name = "question.html"
    question = data_manager.get_record_by_id(question_id, 'question')
    if question is None:
        return render_template(template_name, question_id=question_id)
    answers = data_manager.get_record_by_question_id(question_id, 'answer')
    comments = data_manager.get_record_by_question_id(question_id, 'comment')
    return render_template(template_name, question=question, answers=answers, comments=comments)


@app.route("/question/<question_id>/edit", methods=['GET', 'POST'])
def route_question_edit(question_id):
    question = data_manager.get_question_by_id(question_id)
    if question is None:
        return render_template('question.html', question_id=question_id)
    else:
        return render_template('add_question.html', question=question)


@app.route("/question/<question_id>/new-answer", methods=["GET", "POST"])
def route_add_answer(question_id):
    id_ = data_manager.get_new_id('answer')
    default_vote = 0
    if request.method == "POST":
        new_answer = request.form.to_dict()
        new_answer["id"] = id_+1
        new_answer["submission_time"] = int(time.time())
        new_answer["vote_number"] = default_vote
        new_answer["question_id"] = question_id
        data_manager.insert_new_record('answer', new_answer)
        return redirect(f"/question/{question_id}")
    return render_template("answer.html", parent_id=question_id, parent='question', type='answer')


@app.route("/question/<question_id>/delete")
def route_delete_question(question_id):
    data_manager.delete_by_id('question', question_id)
    return redirect("/")


@app.route("/answer/<answer_id>/delete", methods=['GET', 'POST'])
def route_delete_answer(answer_id):
    if request.method == "POST":
        answer = data_manager.get_record_by_id(answer_id, answer=True)
        question_id = answer["question_id"]
        data_manager.delete_by_id('answer', answer_id,)
        return redirect(url_for("route_question_display", question_id=question_id))
    return redirect("/")


@app.route("/add-question", methods=['GET', 'POST'])
def route_question_add():
    id_ = data_manager.get_new_id('question')
    if request.method == 'POST':
        new_q = request.form.to_dict()
        new_q['id'] = id_+1
        new_q['submission_time'] = int(time.time())
        data_manager.insert_new_record('question', new_q)
        return redirect('/question/%s' % id_)
    else:
        return render_template('add_question.html', id=id_)


@app.route('/question/<question_id>/new-comment', methods=['GET', 'POST'])
def route_add_comment_to_question(question_id):
    if request.method == 'POST':
        message = request.form.get('msg')
        edited_count = request.form.get('edited_count')
        if edited_count is None:
            edited_count = 0
        edited_count += 1
        data_manager.add_comment(message, edited_count, question_id, 'question')
        return redirect(url_for('route_question_display', question_id=question_id))
    return render_template('answer.html', parent_id=question_id, parent='question', type='comment')


@app.route('/answer/<answer_id>/edit', methods=['GET', 'POST'])
def route_edit_answer(answer_id):
    question_id = request.form.get('parent_id')
    if question_id is not None:
        message = request.form.get('msg')
        image = request.form.get('image')
        data_manager.update_answer(message, image, answer_id)
        return redirect(url_for('route_question_display', question_id=question_id))
    answer = data_manager.get_answer_by_id(answer_id)
    return render_template('answer.html', data=answer, id=answer_id, type='answer')


if __name__ == "__main__":
    app.run(debug=True)
