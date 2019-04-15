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


# read data from csv
def read_csv():
    pass


# write data to csv
def write_to_csv():
    pass


def get_question_by_id(question_id):
    questions = connection.read_csv("data/question.csv")
    for question in questions:
        if question["id"] == question_id:
            return question


def get_answers_by_question_id(qustion_id):
    answers = connection.read_csv("data/answer.csv")
    return [x for x in answers if x["question_id"] == qustion_id]


def convert_headers_to_user_friendly(headers):
    for i in range(len(headers)):
        headers[i] = headers[i].capitalize().replace("_", " ")
