import connection
import database_common



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


def update_vote_number(id_, increase_by, answer=False):
    record = get_record_by_id(id_, answer=answer)
    vote_number = int(record["vote_number"])
    record["vote_number"] = vote_number + increase_by
    if answer:
        connection.update_to_csv("data/answer.csv", record, ANSWERS_HEADER)
    else:
        connection.update_to_csv("data/question.csv", record, QUESTIONS_HEADER)


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


def get_record_by_id(id_, answer=False):
    filename = f"data/{'answer' if answer else 'question'}.csv"
    records = connection.read_csv(filename)
    for record in records:
        if record["id"] == id_:
            return record


def get_answers_by_question_id(question_id):
    answers = connection.read_csv("data/answer.csv")
    return [x for x in answers if x["question_id"] == question_id]


def sort_by_any(filename, header_by, reverse_):
    table = connection.read_csv(filename)
    table.sort(key=lambda x: int(x[header_by]) if x[header_by].lstrip(
        "-").isdigit() else x[header_by], reverse=reverse_)
    return table


def delete_by_id(id_to_del, id_type, answer=False):
    filename = f"data/{'answer' if answer else 'question'}.csv"
    table = connection.read_csv(filename)
    table = [x for x in table if x[id_type] != id_to_del]
    for row in table:
        if int(row[id_type]) > int(id_to_del):
            row[id_type] = int(row[id_type]) - 1
    connection.write_data_(
        filename,
        table,
        ANSWERS_HEADER if answer else QUESTIONS_HEADER)


@database_common.connection_handler
def get_data_from_database(cursor, search_phrase):
    cursor.execute('''
                   SELECT DISTINCT ON (title) title, question.message FROM question, answer
                   WHERE title LIKE %(search_phrase)s OR question.message LIKE %(search_phrase)s
                   OR answer.message LIKE %(search_phrase)s AND question.id=question_id;
                   ''',
                   {'search_phrase': search_phrase})
    results = cursor.fetchall()

    return results