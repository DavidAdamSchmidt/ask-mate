import connection


ANSWERS_HEADER = [
    "id",
    "submission_time",
    "vote_number",
    "question_id",
    "message",
    "image"
]


QUESTIONS_HEADER = [
    "id",
    "submission_time",
    "view_number",
    "vote_number",
    "title",
    "message",
    "image"
]



def read_csv(filename):
    return connection.read_csv(filename)


def write_new_to_csv(filename, headers, fieldnames):
    connection.write_new_to_csv(filename, headers, fieldnames)


def update_to_csv(filename, updated_qna, headers):
    connection.update_to_csv(filename, updated_qna, headers)


def get_question_by_id(question_id):
    questions = connection.read_csv("data/question.csv")
    for question in questions:
        if question["id"] == str(question_id):
            return question


def get_answers_by_question_id(question_id):
    answers = connection.read_csv("data/answer.csv")
    return [x for x in answers if x["question_id"] == question_id]
