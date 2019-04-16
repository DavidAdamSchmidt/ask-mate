from flask import Flask, request, redirect, render_template
import data_manager
import time


app = Flask(__name__)

@app.route("/")
@app.route("/list")
def route_questions_list():
    return render_template('index.html')


@app.route("/question/<question_id>")
def route_question_display(question_id):
    template_name = "question.html"
    question = data_manager.get_question_by_id(question_id)
    if question is None:
        return render_template(template_name, question_id=question_id)
    answers = data_manager.get_answers_by_question_id(question_id)
    return render_template(template_name, question=question, answers=answers)


@app.route("/add-question", methods=['GET', 'POST'])
def route_question_add():
    if request.method == 'POST':
        question_id = len(data_manager.read_csv('data/question.csv'))
        submission_time = int(time.time())
        view_number = 0
        vote_number = 0
        title = request.form['title']
        message = request.form['message']
        image = ''
<<<<<<< HEAD
        fieldnames = ['question_id', 'submission_time', 'view_number', 'vote_number',
                      'title', 'message', 'image']
        headers = [question_id, submission_time, view_number, vote_number,
=======
        fieldnames = data_manager.QUESTIONS_HEADER
        headers = [id_num, submission_time, view_number, vote_number,
>>>>>>> 7c83c9cba10f4b0e61ad6f0577764b8e858bbeca
                   title, message, image]
        data_manager.write_to_csv('data/question.csv', headers, fieldnames)
        return redirect('/question/%s' % question_id)
    return render_template('add_question.html')



@app.route("/question/<question_id>/new-answer")
def route_post_answer(question_id):
    pass


if __name__ == "__main__":
    app.run(debug=True, port=5000)
